nextflow.enable.dsl = 2

include { ESKAPE_GEM_PIPELINE } from './workflows/eskape_gem_pipeline.nf'

workflow {

    if (!params.samplesheet) {
        error "Please provide --samplesheet <path/to/samplesheet.csv>"
    }

    samples_ch = Channel
        .fromPath(params.samplesheet)
        .splitCsv(header: true)
        .map { row ->
            if (params.skip_assembly) {
                tuple(row.sample_id, row.species, file(row.assembly))
            } else {
                tuple(row.sample_id, row.species, file(row.reads_1), file(row.reads_2))
            }
        }

    ESKAPE_GEM_PIPELINE(samples_ch)
}
