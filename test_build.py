import json, tempfile, unittest
from pathlib import Path
from build import ROOT, build, validate
class BuildTests(unittest.TestCase):
    def setUp(self):self.config=json.loads((ROOT/'campaign.json').read_text())
    def test_export_includes_real_local_assets(self):
        with tempfile.TemporaryDirectory() as d:
            path=build(ROOT/'campaign.json',Path(d)/'site');self.assertTrue((path/self.config['heroImage']).is_file());self.assertTrue((path/'index.html').is_file())
    def test_missing_outline_fields_block_build(self):
        self.config['headline']=''
        with self.assertRaises(ValueError):validate(self.config)
    def test_bad_destination_and_asset_escape_blocked(self):
        for key,value in [('ctaUrl','javascript:alert(1)'),('heroImage','../../private.png'),('privacyUrl','https://user:pass@example.com')]:
            c={**self.config,key:value}
            with self.assertRaises(ValueError):validate(c)
    def test_unknown_tracker_is_not_silently_claimed_supported(self):
        self.config['tracking']={'tiktok':'123'}
        with self.assertRaises(ValueError):validate(self.config)
    def test_script_like_copy_escaped_in_export(self):
        self.config['headline']='</script><script>alert(1)</script>'
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'campaign.json';f.write_text(json.dumps(self.config));out=build(f,Path(d)/'site');self.assertNotIn('</script>',(out/'config.js').read_text())
if __name__=='__main__':unittest.main()
