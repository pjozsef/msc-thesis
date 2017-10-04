package com.github.pjozsef.thesis.dsp.cli

import com.beust.jcommander.IStringConverter
import com.beust.jcommander.Parameter
import com.beust.jcommander.Parameters

sealed class Command {
    companion object {
        const val TAG = "tag"
        const val WAV = "wav"
        const val SPECTROGRAM = "spectrogram"
        const val SECTION = "section"
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

    @Parameter(names = arrayOf("--colored"), description = "color based on magnitude")
    var colored: Boolean = false
}

@Parameters(commandDescription = "Find the sections denoted by the provided percentiles")
class SectionCommand : Command() {
    @Parameter(required = true, description = "<input wav file>")
    lateinit var files: List<String>

    @Parameter(names = arrayOf("-c", "--chunkSize"), description = "chunk size")
    var chunkSize: Int = 8192

    @Parameter(names = arrayOf("-w", "--windowSize"), description = "window size")
    var windowSize: Int = 5 * 30

    @Parameter(names = arrayOf("-s", "--stepSize"), description = "step size")
    var stepSize: Int = 1

    @Parameter(
            names = arrayOf("-p", "--percentiles"),
            required = true,
            converter = IntListConverter::class,
            description = "percentiles, separated by a comma")
    lateinit var percentiles: List<Int>
}

private class IntListConverter : IStringConverter<Int> {
    override fun convert(value: String) = Integer.parseInt(value)

}