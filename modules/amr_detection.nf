process AMR_DETECTION {
    tag "$sample_id"
    label 'annotation'
    publishDir "${params.outdir}/amr/${sample_id}", mode: 'copy'

    input:
    tuple val(sample_id), val(species), path(faa), path(gff)

    output:
    tuple val(sample_id), path("${sample_id}_amrfinder.tsv"), emit: amr_calls

    script:
    def organism = species.replaceAll(' ', '_')
    """
    amrfinder -p ${faa} -O ${organism} --threads ${task.cpus} -o ${sample_id}_amrfinder.tsv
    """
}
