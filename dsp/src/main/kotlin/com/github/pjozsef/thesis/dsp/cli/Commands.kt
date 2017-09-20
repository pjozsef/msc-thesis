package com.github.pjozsef.thesis.dsp.cli

import com.beust.jcommander.Parameter
import com.beust.jcommander.Parameters

sealed class Command {
    companion object {
        const val TAG = "tag"
        const val WAV = "wav"
        const val SPECTROGRAM = "spectrogram"
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
}