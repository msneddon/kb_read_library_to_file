#include <KBaseCommon.spec>
/*
A KBase module: kb_read_library_to_file

Takes KBaseFile/KBaseAssembly PairedEndLibrary/SingleEndLibrary reads library
workspace object IDs as input and produces a FASTQ files along with file
metadata.

Operational notes:
- All reads files must be in fastq format, and thus provided types or filenames
  must have a case-insensitive .fq or .fastq suffix.
- Reads files are optionally gzipped, and as if so have a case-insensitive .gz
  suffix after the fastq suffix.
- The file type and suffixes are determined from, in order of precedence:
  - the lib?/type field in KBaseFile types
  - the lib?/file/filename or handle?/filename field
  - the shock filename
- If the file types / suffixes do not match the previous rules, the converter
  raises an error.
- If a file has a .gz suffix, it is assumed to be gzipped.
- Files are assumed to be in correct fastq format.

*/

module kb_read_library_to_file {

    /* A ternary. Allowed values are 'false', 'true', or null. Any other
        value is invalid.
     */
     typedef string tern;
    
    /* The workspace object name of a read library, whether of the
       KBaseAssembly or KBaseFile type.
    */
    typedef string read_lib;
    
    /* An absolute output file path prefix. The location given by the path must
        be writable. The suffix of the file will be determined by the
        converter:
        If the file is interleaved, the first portion of the suffix will be
            .int. Otherwise it will be .fwd. for the forward / left reads,
            .rev. for the reverse / right reads, or .sing. for single ended
            reads.
        The next portion of the suffix will be .fastq.
        If a file is in gzip format, the file will end with .gz.
     */
    typedef string file_path_prefix;
    
    /* Input parameters for converting libraries to files.
        string workspace_name - the name of the workspace from which to take
           input.
        mapping<read_lib, file_path_prefix> read_libraries - read library
            objects to convert and the prefix of the file(s) in which the FASTQ
            files will be saved. The set of file_prefixes must be unique.
        tern gzip - if true, gzip any unzipped files. If false, gunzip any
            zipped files. If null or missing, leave files as is unless
            unzipping is required for interleaving or deinterleaving, in which
            case the files will be left unzipped.
        tern interleaved - if true, provide the files in interleaved format if
            they are not already. If false, provide forward and reverse reads
            files. If null or missing, leave files as is.
    */
    typedef structure {
        string workspace_name;
        mapping<read_lib, file_path_prefix> read_libraries;
        tern gzip;
        tern interlaced;
    } ConvertReadLibraryParams;
    
    /* Information about each set of reads.
        The reads file locations:
        string fwd - the path to the forward / left reads.
        string rev - the path to the reverse / right reads.
        string inter - the path to the interleaved reads.
        string sing - the path to the single end reads.
        Only the appropriate fields will be present in the structure.

        Other fields:
        string ref - the workspace reference of the reads file, e.g
            workspace_id/object_id/version.
        tern single_genome - whether the reads are from a single genome or a
            metagenome. null if unknown.
        tern read_orientation_outward - whether the read orientation is outward
            from the set of primers. Always false for singled ended reads. null
            if unknown.
        string sequencing_tech - the sequencing technology used to produce the
            reads. null if unknown.
        KBaseCommon.StrainInfo strain - information about the organism strain
            that was sequenced. null if unavailable.
        KBaseCommon.SourceInfo source - information about the organism source.
            null if unavailable.
        float insert_size_mean - the mean size of the genetic fragments. null
            if unavailable or single end read.
        float insert_size_std_dev - the standard deviation of the size of the
            genetic fragments. null if unavailable or single end read.
        int read_count - the number of reads in the this dataset. null if
            unavailable.
        int read_size - the total size of the reads, in bases. null if
            unavailable.
        float gc_content - the GC content of the reads. null if
            unavailable.
     */
    typedef structure {
        string fwd;
        string rev;
        string inter;
        string sing;
        string ref;
        tern single_genome;
        tern read_orientation_outward;
        string sequencing_tech;
        KBaseCommon.StrainInfo strain;
        KBaseCommon.SourceInfo source;
        float insert_size_mean;
        float insert_size_std_dev;
        int read_count;
        int read_size;
        float gc_content;
    } ConvertedReadLibrary;

    /* The output of the convert method.
        mapping<read_lib, ConvertedReadLibrary> files - a mapping
            of the read library workspace object names to information
            about the converted data for each library.
     */
    typedef structure {
        mapping<read_lib, ConvertedReadLibrary> files;
    } ConvertReadLibraryOutput;
   
    /* Convert read libraries to files */
    funcdef convert_read_library_to_file(ConvertReadLibraryParams params)
        returns(ConvertReadLibraryOutput output) authentication required;
};