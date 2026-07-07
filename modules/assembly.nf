process ASSEMBLY {
    tag "$sample_id"
    label 'assembly'
    publishDir "${params.outdir}/assembly/${sample_id}", mode: 'copy'

    input:
    tuple val(sample_id), val(species), path(reads_1), path(reads_2)

    output:
    tuple val(sample_id), val(species), path("${sample_id}_assembly.fasta"), emit: assembly

    script:
    """
    unicycler -1 ${reads_1} -2 ${reads_2} -o ${sample_id}_unicycler --threads ${task.cpus}
    cp ${sample_id}_unicycler/assembly.fasta ${sample_id}_assembly.fasta
    """
}
