# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ..preprocess import Hist


def test_Hist_inputs():
    input_map = dict(
        args=dict(argstr="%s",),
        bin_width=dict(argstr="-binwidth %f",),
        environ=dict(nohash=True, usedefault=True,),
        in_file=dict(
            argstr="-input %s",
            copyfile=False,
            extensions=None,
            mandatory=True,
            position=1,
        ),
        mask=dict(argstr="-mask %s", extensions=None,),
        max_value=dict(argstr="-max %f",),
        min_value=dict(argstr="-min %f",),
        nbin=dict(argstr="-nbin %d",),
        out_file=dict(
            argstr="-prefix %s",
            extensions=None,
            keep_extension=False,
            name_source=["in_file"],
            name_template="%s_hist",
        ),
        out_show=dict(
            argstr="> %s",
            extensions=None,
            keep_extension=False,
            name_source="in_file",
            name_template="%s_hist.out",
            position=-1,
        ),
        showhist=dict(argstr="-showhist", usedefault=True,),
    )
    inputs = Hist.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_Hist_outputs():
    output_map = dict(out_file=dict(extensions=None,), out_show=dict(extensions=None,),)
    outputs = Hist.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
