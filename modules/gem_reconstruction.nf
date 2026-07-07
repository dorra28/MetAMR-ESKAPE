process GEM_RECONSTRUCTION {
    tag "$sample_id"
    label 'gem'
    publishDir "${params.outdir}/gems/${sample_id}", mode: 'copy'

    input:
    tuple val(sample_id), val(species), path(faa), path(gff)

    output:
    tuple val(sample_id), path("${sample_id}_draft.xml"), emit: draft_model

    script:
    def gram_flag = (params.gram == 'gramneg') ? '--gramneg' : (params.gram == 'grampos') ? '--grampos' : ''
    """
    carve ${faa} -o ${sample_id}_draft.xml --gapfill ${params.media} ${gram_flag} --fbc2
    """
}
