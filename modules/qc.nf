process QC {
    tag "$sample_id"
    label 'qc'
    publishDir "${params.outdir}/qc/${sample_id}", mode: 'copy'

    input:
    tuple val(sample_id), val(species), path(reads_1), path(reads_2)

    output:
    tuple val(sample_id), val(species), path("${sample_id}_R1.clean.fastq.gz"), path("${sample_id}_R2.clean.fastq.gz"), emit: reads
    path "${sample_id}.fastp.json"
    path "${sample_id}.fastp.html"

    script:
    """
    fastp \\
        -i ${reads_1} -I ${reads_2} \\
        -o ${sample_id}_R1.clean.fastq.gz -O ${sample_id}_R2.clean.fastq.gz \\
        --detect_adapter_for_pe --thread ${task.cpus} \\
        --json ${sample_id}.fastp.json --html ${sample_id}.fastp.html
    """
}
