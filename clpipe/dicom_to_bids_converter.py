import click
from .batch_manager import BatchManager, Job


@click.command()
@click.argument('dicomdirectory')
@click.argument('outputfile')
@click.option('-batchConfig', default="slurmUNCConfigHeudiconv.json")
def dicom_to_nifti_to_bids_converter_setup(dicomdirectory, outputfile, batchconfig):
    # TODO: This function should run heudiconv with a default heuristic file
    # on one subject, pull the scan info file out of the directory and put it
    # in the output file, and then delete the test directory that was generated by heudiconv.
    # The key difficulty will be in copying the scaninfo file after heudiconv is done.
    # this potentially could be done with a dependency statement in a batch command.
    # To submit batch commmands, use the BatchManager class

    batch_manager = BatchManager(batchconfig)

    # You can write add jobs to the Batch manager by first making a job:
    # job1 = Job(jobID, submission string)
    # And then adding it to the batch manager
    # batch_manager.addjob(job1)

    # To submit all jobs:
    # batch_manager.compilejobstrings()
    # batch_manager.submit_jobs()
    # To print the current set of job strings:
    # batch_manager.print_jobs()

    return 0
