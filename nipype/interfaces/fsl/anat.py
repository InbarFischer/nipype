from ...utils.filemanip import fname_presuffix, split_filename, copyfile
from ..base import (
    TraitedSpec,
    isdefined,
    File,
    Directory,
    InputMultiPath,
    OutputMultiPath,
    traits,
)
from .base import FSLCommand, FSLCommandInputSpec, Info


import os

class FSLAnatInputSpec(FSLCommandInputSpec):

    input_img = File(
        exists=True,
        desc="filename of input image (for one image only)",
        argstr="-i %s",
        position=-1,
        mandatory =True,
        xor = ['input_directory']
    )

    input_directory = Directory(
        exists=True,
        desc="directory name for existing .anat directory where this script will be run in place",
        argstr="-d %s",
        position=-1,
        mandatory =True,
        xor = ['input_img']
    )

    output_directory = Directory(
        exists = True,
        desc = 'basename of directory for output (default is input image basename followed by .anat)',
        argstr = '-o %s',
        mandatory = False,
    )

    weakbias = traits.Bool(desc="used for images with little and/or smooth bias fields",
                           argstr="--weakbias"
                           )

    clobber = traits.Bool(desc="if .anat directory exist (as specified by -o or default from -i) then delete it and make a new one",
                           argstr="--clobber"
                           )

    noreorient = traits.Bool(desc="turn off step that does reorientation 2 standard (fslreorient2std)",
                           argstr="--noreorient")

    nocrop = traits.Bool(desc="turn off step that does automated cropping (robustfov)",
                           argstr="--nocrop"
                           )

    nobias = traits.Bool(desc="turn off steps that do bias field correction (via FAST)",
                           argstr="--nobias"
                           )

    noreg = traits.Bool(desc="turn off steps that do registration to standard (FLIRT and FNIRT)",
                           argstr="--noreg"
                           )

    nononlinreg = traits.Bool(desc="turn off step that does non-linear registration (FNIRT)",
                           argstr="--nononlinreg"
                           )

    noseg = traits.Bool(desc="turn off step that does tissue-type segmentation (FAST)",
                           argstr="--noseg"
                           )

    nosubcortseg = traits.Bool(desc="turn off step that does sub-cortical segmentation (FIRST)",
                           argstr="--nosubcortseg"
                           )

    image_type = traits.Str('image_type',
                           desc="specify the type of image (choose one of T1 T2 PD - default is T1)",
                           argstr="-t %s"
                           )

    s = traits.Int(desc="specify the value for bias field smoothing (the -l option in FAST)",
                           argstr="-s %d")

    nosearch = traits.Bool(desc="specify that linear registration uses the -nosearch option (FLIRT)",
                           argstr="--nosearch"
                           )

    betfparam = traits.Float(desc="specify f parameter for BET (only used if not running non-linear reg and also wanting brain extraction done)",
                           argstr="--betfparam %.2f"
                           )

    nocleanup = traits.Bool(desc="do not remove intermediate files",
                           argstr="--nocleanup"
                           )

class FSLAnatOutputSpec(TraitedSpec):
    Out = File(exists=False, desc= r"Contains either the T1, T2 or PD image (according to the -t input option) after cropping and\or orientation.")
    Out_orig = File(exists=False,  desc= r"The original image (exists if the image was cropped and\or reoriented)")
    Out_fullfov= File(exists=False,  desc= r"The image in full field-of-view (exists if the image was cropped and\or reoriented)" )
    Out_orig2std = File(exists=False,  desc= "")
    Out_noroi2roi = File(exists=False, desc= "")
    Out_biascorr = File(exists=False,  desc= "")
    Out_to_MNI_lin = File(exists=False,  desc= "Linear registration output")
    Out_to_MNI_nonlin = File(exists=False, desc= "Non-linear registration output")
    Out_to_MNI_nonlin_field = File(exists=False, desc= "Non-linear warp field")
    Out_to_MNI_nonlin_jac = File(exists=False, desc= "Jacobian of the non-linear warp field")
    Out_vols = File(exists=False, desc= "A file containing a scaling factor and brain volumes, based on skull-contrained registration, "
                                        "suitable for head-size normalisation (as the scaling is based on the skull size, not the brain size")
    Out_biascorr_brain = File(exists=False, desc= "")
    Out_biascorr_brain_mask = File(exists=False,  desc= "")
    Out_fast_pve_0 = File(exists=False, desc= "Cerebral spinal fluid segmentation")
    Out_fast_pve_1 = File(exists=False,  desc="Gray matter segmentation")
    Out_fast_pve_2 = File(exists=False,  desc="White matter segmentation")
    Out_fast_pveseg = File(exists=False,  desc="A summary image showing the tissue with the greatest partial volume fraction per voxel")
    Out_subcort_seg = File(exists=False, desc="Summary image of all sub-cortical segmentations")
    first_results = Directory(desc="") #TODO: add path?
    Out_first_all_fast_firstseg = File(exists=False,  desc="")
    Out_biascorr_to_std_sub = File(exists=False, desc="A transformation matrix of the sub-cortical optimised MNI registration")



class FSLAnat(FSLCommand):
    _cmd = "fsl_anat"
    input_spec = FSLAnatInputSpec
    output_spec = FSLAnatOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        if not isdefined(self.inputs.image_type):
            out_type = 'T1'
        else:
            out_type = self.inputs.image_type
        if  isdefined(self.inputs.output_directory):
            out_directory = self.inputs.output_directory + ".anat"
        elif isdefined(self.inputs.input_directory):
            out_directory = self.inputs.input_directory

        else:
            out_directory = FSLAnat.remove_ext(self.inputs.input_img) + ".anat"
        res_path = os.path.join(os.getcwd(),out_directory)
        res_files = [os.path.join(res_path, f) for f in os.listdir(res_path) if os.path.isfile(os.path.join(res_path, f))]
        res_dict = {split_filename(k)[1]:k for k in res_files}
        for k in set(outputs.keys()):
            corrected_name = k.replace('Out',out_type,1)
            if corrected_name in res_dict.keys():
                outputs[k] = res_dict[corrected_name]

            #else:
                #outputs[k] = None
        return outputs
    @staticmethod
    def remove_ext(s):
        last_dot = s.rfind('.')
        if  last_dot != -1:
            return s[:last_dot]
        else:
            return s