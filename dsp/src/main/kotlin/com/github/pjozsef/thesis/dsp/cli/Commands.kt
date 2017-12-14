package com.github.pjozsef.thesis.dsp.cli

import com.beust.jcommander.IStringConverter
import com.beust.jcommander.Parameter
import com.beust.jcommander.Parameters
import java.io.File


sealed class Command {
    companion object {
        const val TAG = "tag"
        const val WAV = "wav"
        const val SPECTROGRAM = "spectrogram"
        const val SECTION = "section"
        const val LIST = "list"
        const val EXPORT = "export"
        const val EXPORT_LIST = "exportlist"
    }
}

@Parameters(commandDescription = "List the artist, title and album tags of the MP3 file")
class TagCommand : Command() {
    @Parameter(required = true, description = "<input mp3 file>")
    lateinit var files: List<String>
}

@Parameters(commandDescription = "Convert the given mp3 file to wav")
class WavCommand : Command() {
    @Parameter(required = true, description = "<input mp3 file>")
    lateinit var files: List<String>
}

@Parameters(commandDescription = "Create the spectrogram image for the given wav file")
class SpectrogramCommand : Command() {
    @Parameter(required = true, description = "<input wav file>")
    lateinit var files: List<String>

    @Parameter(names = arrayOf("-c", "--chunkSize"), description = "chunk size")
    var chunkSize: Int = 8192

    @Parameter(names = arrayOf("-h", "--height"), description = "crop image height, suggested value: 800")
    var height: Int? = null

    @Parameter(
            names = arrayOf("-m", "--markerLines"),
            converter = DoubleListConverter::class,
            description = "draw lines at the given frequencies")
    var markerLines: List<Double> = listOf()

    @Parameter(names = arrayOf("--colored"), description = "color based on magnitude")
    var colored: Boolean = false
}

@Parameters(commandDescription = "Find the sections denoted by the provided percentiles")
class SectionCommand : Command() {
    private val samplesPerSecond = 5

    fun validate() {
        require(export || output) { "Either export or print must be turned on! (-e -p)" }
    }

    @Parameter(required = true, description = "<input wav file>")
    lateinit var files: List<String>

    @Parameter(names = arrayOf("-c", "--chunkSize"), description = "chunk size")
    var chunkSize: Int = 8192

    @Parameter(names = arrayOf("-h", "--height"), description = "crop image height, suggested value: 800")
    var height: Int? = null

    @Parameter(names = arrayOf("-w", "--windowSize"), description = "window size in seconds")
    var windowSize: Int = 20
        get() = field * samplesPerSecond

    @Parameter(names = arrayOf("-s", "--stepSize"), description = "step size")
    var stepSize: Int = 1

    @Parameter(names = arrayOf("-e", "--export"), description = "export the sections as png images")
    var export: Boolean = false

    @Parameter(names = arrayOf("-o", "--output"), description = "print the sections to the console")
    var output: Boolean = false

    @Parameter(
            names = arrayOf("-p", "--percentiles"),
            required = true,
            converter = IntListConverter::class,
            description = "percentiles, separated by a comma")
    lateinit var percentiles: List<Int>
}

@Parameters(commandDescription = "Export data from wav/mp3 file. Chunk size: 8192, height: 800, window size: 20, step size: 1, percentiles: 20,40,60,80,100")
class ExportCommand : Command() {
    @Parameter(required = true, description = "<input wav file>")
    lateinit var files: List<String>

    @Parameter(
            names = arrayOf("-o", "--outputDirectory"),
            description = "Output folder, defaults to current working directory",
            converter = FileConverter::class)
    var outputDirectory = File(".")
        set(value) {
            field = value.absoluteFile.normalize()
        }

    val chunkSize = 8192
    val height = 800
    val windowSize = 20
    val stepSize = 1
    val export = true
    val output = false
    val percentiles = listOf(20, 40, 60, 80, 100)
}

@Parameters(commandDescription = "Export all data defined in txt files. Calls export for each of them.")
class ExportListCommand : Command() {
    @Parameter(required = true, description = "<input txt files>")
    lateinit var files: List<String>

    @Parameter(
            names = arrayOf("-p", "--previousProgress"),
            description = "<previousProgress of previous command run>")
    var previousProgress: String? = null

    @Parameter(
            names = arrayOf("-o", "--outputDirectory"),
            description = "Output folder, defaults to current working directory",
            converter = FileConverter::class)
    var outputDirectory = File(".")
        set(value) {
            field = value.absoluteFile.normalize()
        }

    val currentProgress: File by lazy {
        outputDirectory.resolve("previousProgress")
    }
}

@Parameters(commandDescription = "Recursively list the MP3 files in the given folders")
class ListCommand : Command() {
    @Parameter(required = true, description = "<input folders>")
    lateinit var folders: List<String>

    @Parameter(names = arrayOf("-i", "--ignoreErrors"), description = "List the path of the mp3 file")
    var ignoreErrors: Boolean = false

    @Parameter(names = arrayOf("--path"), description = "List the path of the mp3 file")
    var listPath: Boolean = false

    @Parameter(names = arrayOf("--artist"), description = "List the artist of the mp3 file")
    var listArtist: Boolean = false

    @Parameter(names = arrayOf("--album"), description = "List the album of the mp3 file")
    var listAlbum: Boolean = false

    @Parameter(names = arrayOf("--song"), description = "List the song of the mp3 file")
    var listSong: Boolean = false

    fun validate() {
        require(listPath || listArtist || listAlbum || listSong) {
            "At least one switch must be turned on from [path, artist, album, song]"
        }
    }
}

private class IntListConverter : IStringConverter<Int> {
    override fun convert(value: String) = Integer.parseInt(value)
}

private class DoubleListConverter : IStringConverter<Double> {
    override fun convert(value: String) = value.toDouble()
}

private class FileConverter : IStringConverter<File> {
    override fun convert(value: String) = File(value)
}