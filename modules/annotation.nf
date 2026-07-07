process ANNOTATION {
    tag "$sample_id"
    label 'annotation'
    publishDir "${params.outdir}/annotation/${sample_id}", mode: 'copy'

    input:
    tuple val(sample_id), val(species), path(assembly)

    output:
    tuple val(sample_id), val(species), path("${sample_id}.faa"), path("${sample_id}.gff3"), emit: annotated

    script:
    """
    bakta --db ${params.bakta_db} --prefix ${sample_id} --threads ${task.cpus} ${assembly}
    cp ${sample_id}/${sample_id}.faa ${sample_id}.faa
    cp ${sample_id}/${sample_id}.gff3 ${sample_id}.gff3
    """
}
