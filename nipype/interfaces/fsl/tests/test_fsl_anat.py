from nipype.interfaces.fsl.anat import FSLAnat
from ..base import isdefined
# test the cmdline of fsl_anat
def test_cmdline_fsl_anat(create_files_in_directory):
    filelist = create_files_in_directory
    anat = FSLAnat()
    # make sure right command gets called
    assert anat.cmd == "fsl_anat"

    # .inputs based parameters setting
    anat.inputs.input_img = filelist[0]
    anat.inputs.output_directory = "outdir"
    anat.inputs.image_type = 'T1'
    anat.inputs.noreorient = True
    anat.inputs.nocrop = True
    anat.inputs.nobias = True
    anat.inputs.noseg = True
    anat.inputs.noreg = True
    anat.inputs.nononlinreg = True
    anat.inputs.nosubcortseg = True
    anat.inputs.nosearch = True

    assert (
        anat.cmdline == 'fsl_anat -t T1 --nobias --nocrop --nononlinreg --noreg --noreorient --nosearch --noseg --nosubcortseg -o outdir -i {0}'.format(filelist[0])
    )


# asserts that the run crashes if no mandatory argument is given, or if both an image input and a directory is given
@pytest.mark.skipif(no_fsl(), reason="fsl is not installed")
def check_mandatory(create_files_in_directory):
    anat = FSLAnat()
    anat.inputs.output_directory = "outdir"
    anat.inputs.image_type = 'T1'
    anat.inputs.noreorient = True
    anat.inputs.nocrop = True
    anat.inputs.nobias = True
    anat.inputs.noseg = True
    anat.inputs.noreg = True
    anat.inputs.nononlinreg = True
    anat.inputs.nosubcortseg = True
    anat.inputs.nosearch = True

    # No mandatory input is given
    with pytest.raises(ValueError):
        anat.run()

    # Conflicting mandatory inputs are given
    with pytest.raises(OSError):
        filelist = create_files_in_directory
        anat.inputs.input_img = filelist[0]
        anat.inputs.input_directory = filelist[1]

@pytest.mark.skipif(no_fsl(), reason="fsl is not installed")
def check_nononlinreg_and_betfparam(create_files_in_directory):
    anat = FSLAnat()
    filelist = create_files_in_directory
    anat.inputs.input_img = filelist[0]
    # betfparam and nononlinreg flags cannot both be active
    with pytest.raises(OSError):
        anat.inputs.nononlinreg = True
        anat.inputs.betfparam = True


# Tests whether some basic outputs exist
@pytest.mark.skipif(no_fsl(), reason="fsl is not installed")
def test_basic_outputs(create_files_in_directory):
    anat = FSLAnat()
    filelist = create_files_in_directory
    anat.inputs.input_img = filelist[0]
    anat.inputs.noreorient = True
    anat.inputs.nocrop = True
    anat.inputs.nobias = True
    anat.inputs.noseg = True
    anat.inputs.noreg = True
    anat.inputs.nononlinreg = True
    anat.inputs.nosubcortseg = True
    anat.inputs.nosearch = True
    outputs = anat.run().outputs
    assert isdefined(outputs.Out) and isdefined(outputs.Out_biascorr)