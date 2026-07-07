include { QC }                 from '../modules/qc.nf'
include { ASSEMBLY }           from '../modules/assembly.nf'
include { ANNOTATION }         from '../modules/annotation.nf'
include { AMR_DETECTION }      from '../modules/amr_detection.nf'
include { GEM_RECONSTRUCTION } from '../modules/gem_reconstruction.nf'

workflow ESKAPE_GEM_PIPELINE {

    take:
    samples_ch   // tuple: sample_id, species, reads_1/assembly, [reads_2]

    main:
    if (!params.skip_assembly) {
        qc_out   = QC(samples_ch)
        assembled = ASSEMBLY(qc_out.reads)
    } else {
        assembled = samples_ch
    }

    annotated = ANNOTATION(assembled)
    amr_calls = AMR_DETECTION(annotated.annotated)
    gems      = GEM_RECONSTRUCTION(annotated.annotated)

    emit:
    annotated = annotated.annotated
    amr_calls = amr_calls.amr_calls
    gems      = gems.draft_model
}
