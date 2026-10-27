import hashlib
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/pptx-studio/scripts'
TEST_TMP=ROOT/'.test-output'
TEST_TMP.mkdir(exist_ok=True)
def new_tempdir():
    item=tempfile.TemporaryDirectory(dir=TEST_TMP)
    if not Path(item.name).resolve().is_relative_to(TEST_TMP.resolve()):
        raise RuntimeError('Unexpected test directory')
    return item
sys.path.insert(0,str(SCRIPTS))
from plan import build_plan,load_catalog,parse_slides
from inspect_pptx import inspect,InspectionError
from fixtures import make_deck,shape,table,group,REL,R


class RoutingTests(unittest.TestCase):
    def test_catalog_guides_are_installation_relative(self):
        catalog=load_catalog()
        self.assertEqual(len({r['id'] for r in catalog['directions']}),7)
        self.assertTrue(all((ROOT/'skills/pptx-studio/references'/r['guide']).is_file() for r in catalog['directions']))

    def test_icon_only_scope_does_not_expand_to_content(self):
        plan=build_plan('edit',['icons'],source='deck.pptx',slides='5-8',slide_count=16)
        self.assertEqual(plan['directions'],['icons'])
        self.assertEqual(plan['scope']['slides'],[5,6,7,8])
        self.assertEqual(plan['references'],['references/icons.md','references/verification.md'])

    def test_explicit_bilingual_choices_combine_and_deduplicate(self):
        plan=build_plan('edit',['图标增强','Layout and relationships','icons'],source='deck.pptx')
        self.assertEqual(plan['directions'],['icons','layout'])

    def test_audit_without_direction_does_not_request_mutation(self):
        plan=build_plan('audit',source='deck.pptx')
        self.assertEqual(plan['operation'],'audit')
        self.assertEqual(plan['directions'],[])

    def test_new_deck_default_needs_material_and_chooses_basic_directions(self):
        with self.assertRaises(ValueError):build_plan('create')
        plan=build_plan('create',topic='Synthetic agent workshop')
        self.assertEqual(plan['directions'],['content','layout','style'])

    def test_invalid_selections_fail_instead_of_silently_clamping(self):
        for selection in ['0','-1','4-2','1,,2','1-','2.5','100001']:
            with self.subTest(selection=selection),self.assertRaises(ValueError):parse_slides(selection,16)
        with self.assertRaises(ValueError):parse_slides('17',16)
        with self.assertRaises(ValueError):build_plan('edit',['unknown'],source='deck.pptx')
        with self.assertRaises(ValueError):build_plan('edit',['icons'])

    def test_one_based_mixed_ranges(self):
        self.assertEqual(parse_slides('1-3,2,6',6),[1,2,3,6])
        self.assertIsNone(parse_slides('all',6))

    def test_plan_cli_writes_an_explicit_plan(self):
        with new_tempdir() as folder:
            dest=Path(folder)/'plan.json'
            result=subprocess.run([sys.executable,str(SCRIPTS/'plan.py'),'--operation','edit','--directions','icons','layout','--source','deck.pptx','--slides','2','--output',str(dest)],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(dest.read_text(encoding='utf-8'))['scope']['slides'],[2])


    def test_plan_cannot_overwrite_source_material(self):
        with new_tempdir() as folder:
            source=Path(folder)/'material.pptx';source.write_bytes(b'original material')
            result=subprocess.run([sys.executable,str(SCRIPTS/'plan.py'),'--operation','edit','--directions','icons','--source',str(source),'--output',str(source)],capture_output=True)
            self.assertEqual(result.returncode,2)
            self.assertEqual(source.read_bytes(),b'original material')

    def test_skill_helpers_run_from_an_independent_installation(self):
        with new_tempdir() as folder:
            dest=Path(folder)/'pptx-studio'
            shutil.copytree(SCRIPTS.parent,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            result=subprocess.run([sys.executable,str(dest/'scripts/plan.py'),'--list'],cwd=folder,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(len(json.loads(result.stdout)['directions']),7)
            deck=make_deck(Path(folder)/'sample.pptx')
            result=subprocess.run([sys.executable,str(dest/'scripts/inspect_pptx.py'),str(deck)],cwd=folder,capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=new_tempdir()
        self.root=Path(self.tmp.name)

    def tearDown(self):self.tmp.cleanup()

    def deck(self,*args,**kwargs):return make_deck(self.root/'sample.pptx',*args,**kwargs)

    def codes(self,report):return [f['code'] for f in report['findings']]

    def test_clean_deck_is_read_only_and_never_claims_visual_validation(self):
        path=self.deck();before=path.read_bytes();report=inspect(path)
        self.assertEqual(path.read_bytes(),before)
        self.assertEqual(report['source_sha256'],hashlib.sha256(before).hexdigest())
        self.assertEqual(report['summary']['error_count'],0)
        self.assertEqual(report['visual_verification']['status'],'not_checked')

    def test_repeated_labels_in_different_locations_are_valid(self):
        report=inspect(self.deck([shape(2,'Shared label',x=1)+shape(3,'Shared label',x=6)]))
        self.assertNotIn('possible_duplicate_text_layers',self.codes(report))
        self.assertNotIn('possible_text_overlap',self.codes(report))

    def test_coincident_repeated_text_is_flagged(self):
        report=inspect(self.deck([shape(2,'Repeated')+shape(3,'Repeated')]))
        self.assertIn('possible_duplicate_text_layers',self.codes(report))

    def test_table_paragraph_and_preview_text_layer_regression(self):
        # The duplicated box contains one paragraph, not the entire two-paragraph cell.
        content=table()+shape(3,'现象：复现条件',x=2.2,y=2.15,w=2.6,h=.3)
        report=inspect(self.deck([content]))
        matches=[f for f in report['findings'] if f['code']=='possible_duplicate_text_layers']
        self.assertEqual(len(matches),1)
        self.assertIn('2:r1c1',matches[0]['object_ids'])
        report=inspect(self.deck([table()]))
        self.assertNotIn('possible_duplicate_text_layers',self.codes(report))

    def test_different_overlapping_text_is_a_review_warning(self):
        report=inspect(self.deck([shape(2,'First')+shape(3,'Second')]))
        self.assertIn('possible_text_overlap',self.codes(report))
        self.assertEqual(report['summary']['error_count'],0)

    def test_duplicate_object_ids_are_detected(self):
        report=inspect(self.deck([shape(2,'First',x=1)+shape(2,'Second',x=6)]))
        self.assertIn('duplicate_shape_ids',self.codes(report))

    def test_out_of_bounds_objects_are_located(self):
        report=inspect(self.deck([shape(2,'Outside',x=14)]))
        finding=next(f for f in report['findings'] if f['code']=='object_out_of_bounds')
        self.assertEqual(finding['page'],1)
        self.assertEqual(finding['object_ids'],['2'])

    def test_presentation_order_and_selected_pages(self):
        path=self.deck([shape(2,'Outside',x=14),shape(2,'Second')],parts=['ppt/slides/slide10.xml','ppt/slides/slide2.xml'])
        report=inspect(path,'2')
        self.assertEqual(report['slides'][0]['part'],'ppt/slides/slide2.xml')
        self.assertEqual(report['summary']['slides_inspected'],1)
        self.assertNotIn('object_out_of_bounds',self.codes(report))

    def test_group_coordinates_are_transformed(self):
        content=group(shape(2,'Grouped',x=0,y=0,w=5,h=5))
        report=inspect(self.deck([content]))
        obj=next(o for o in report['slides'][0]['objects'] if o['id']=='2')
        self.assertEqual(obj['box_inches'],[7.0,1.0,1.0,1.0])
        self.assertNotIn('object_out_of_bounds',self.codes(report))

    def test_rotation_is_disclosed_instead_of_falsely_measured(self):
        report=inspect(self.deck([shape(2,'Rotated',rotation=5400000)]))
        self.assertIn('rotated_geometry',report['slides'][0]['unsupported_features'])

    def test_missing_internal_resource_but_not_external_link(self):
        rels=f'<Relationships xmlns="{REL}"><Relationship Id="img" Type="{R}/image" Target="../media/missing.png"/><Relationship Id="web" Type="{R}/hyperlink" Target="https://example.com/" TargetMode="External"/></Relationships>'
        report=inspect(self.deck(extra={'ppt/slides/_rels/slide1.xml.rels':rels}))
        missing=[f for f in report['findings'] if f['code']=='missing_relationship_target']
        self.assertEqual(len(missing),1)

    def test_entity_declarations_are_rejected_without_reading_external_files(self):
        bad='<!DOCTYPE p:presentation [<!ENTITY data SYSTEM "file:///private">]><p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>'
        with self.assertRaises(InspectionError):inspect(self.deck(extra={'ppt/presentation.xml':bad}))

    def test_invalid_page_is_not_a_partial_success(self):
        with self.assertRaises(ValueError):inspect(self.deck(),'2')

    def test_cli_cannot_overwrite_its_input_with_a_report(self):
        path=self.deck();before=path.read_bytes()
        result=subprocess.run([sys.executable,str(SCRIPTS/'inspect_pptx.py'),str(path),'--output',str(path)],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(result.returncode,2)
        self.assertEqual(path.read_bytes(),before)

    def test_cli_reports_duplicate_error_and_strict_warning_status(self):
        path=self.deck([shape(2,'Repeated')+shape(3,'Repeated')])
        command=[sys.executable,str(SCRIPTS/'inspect_pptx.py'),str(path)]
        result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(result.returncode,1)
        self.assertEqual(json.loads(result.stdout)['visual_verification']['status'],'not_checked')
        path=self.deck([shape(2,'Outside',x=14)])
        self.assertEqual(subprocess.run(command,capture_output=True).returncode,0)
        self.assertEqual(subprocess.run(command+['--strict'],capture_output=True).returncode,1)


if __name__=='__main__':unittest.main()
