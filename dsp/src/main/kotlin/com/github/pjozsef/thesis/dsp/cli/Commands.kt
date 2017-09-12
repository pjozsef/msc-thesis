package com.github.pjozsef.thesis.dsp.cli

import com.beust.jcommander.Parameter
import com.beust.jcommander.Parameters

sealed class Command {
    companion object {
        const val ID3 = "id3"
        const val WAV = "wav"
    }
}

@Parameters(commandDescription = "List the artist, title and album tags of the MP3 file")
class Id3Command : Command() {
    @Parameter(required = true, description = "<input mp3 file>")
    lateinit var files: List<String>
}

@Parameters(commandDescription = "Convert the given mp3 file to wav")
class WavCommand : Command() {
    @Parameter(required = true, description = "<input mp3 file>")
    lateinit var files: List<String>
}