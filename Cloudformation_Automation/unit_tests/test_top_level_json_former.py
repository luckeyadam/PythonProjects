from cloudformation_operations import top_level_json_former


def test_get_formation_telmplate():
    output = top_level_json_former.get_formation_telmplate()
    assert "AWSTemplateFormatVersion" in output
