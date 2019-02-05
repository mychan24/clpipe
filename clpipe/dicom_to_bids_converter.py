import click
import json
from .batch_manager import BatchManager,Job

@click.command()
@click.argument('subject', nargs=1, required=True, default=None)
@click.argument('session', nargs = 1, required=True, default=None)
@click.argument('dicomdirectory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.argument('outputfile', type=click.Path(exists=True, dir_okay=False, file_okay=True), default = None)
@click.option('-logOutputDir', type=click.Path(exists=True, dir_okay=True, file_okay=False), default = None)
@click.option('-batchConfig', type=click.Path(dir_okay=False, file_okay=True), default = "slurmUNCConfigHeudiconv.json")
@click.option('-submit/-save', default=False)
def dicom_to_nifti_to_bids_converter_setup(subject = None, session = None, dicomdirectory=None, outputfile=None,
                                           logoutputdir = None, batchconfig = None, submit=False):

    #TODO: This function should run heudiconv with a default heuristic file
    # on one subject, pull the scan info file out of the directory and put it
    # in the output file, and then delete the test directory that was generated by heudiconv.
    # The key difficulty will be in copying the scaninfo file after heudiconv is done.
    # this potentially could be done with a dependency statement in a batch command.
    # To submit batch commmands, use the BatchManager class

    #Do I need to update config file with date ran for just this? Or validate after? It doesn't seem any of this is going in
    #config = ConfigParser()
    #config.config_updater(configfile)

    heudiconv_string = '''module add heudiconv \n heudiconv -d {dicomdirectory}/sub-{subject}/ses-{sess}/* -s {subject} '''\
    ''' -ss {sess} -f convertall -o {dicomdirectory}/test/ -b --minmeta \n cp {dicomdirectory}/test/ '''\
    '''.heudiconv/*/dicominfo_ses-{sess}.tsv {outputfile} \n rm -rf {dicomdirectory}/test/'''
    #Turns out -c is the type of converter to use. It doesn't say anywhere what the default is, but I assume it's dcm2niix.
    #I have seen other examples of people using other converters, but for now I think we can get rid of it

    batch_manager = BatchManager(batchconfig,logoutputdir)
    job1 = Job("heudiconv_setup", heudiconv_string.format(
        dicomdirectory=dicomdirectory,
        subject=subject,
        sess=session,
        outputfile = outputfile,
    ))

    batch_manager.addjob(job1)
    batch_manager.compilejobstrings()
    if submit:
        batch_manager.submit_jobs()
    else:
        batch_manager.print_jobs()



    return 0