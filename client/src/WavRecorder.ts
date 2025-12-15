export class WavRecorder {
    private audioContext: AudioContext | null = null;
    private mediaStream: MediaStream | null = null;
    private scriptProcessor: ScriptProcessorNode | null = null;
    private source: MediaStreamAudioSourceNode | null = null;
    private buffers: Float32Array[] = [];
    private recordingLength: number = 0;
    private sampleRate: number = 0;
    private isRecording: boolean = false;

    async start(): Promise<void> {
        this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
        this.sampleRate = this.audioContext.sampleRate;
        this.buffers = [];
        this.recordingLength = 0;

        try {
            this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        } catch (error) {
            console.error('Error accessing microphone:', error);
            throw error;
        }

        this.source = this.audioContext.createMediaStreamSource(this.mediaStream);

        // Use ScriptProcessorNode (deprecated but widely supported for this simple use case without worklets)
        // bufferSize 4096 gives about ~93ms latency at 44.1kHz, which is fine for recording
        this.scriptProcessor = this.audioContext.createScriptProcessor(4096, 1, 1);

        this.scriptProcessor.onaudioprocess = (event) => {
            if (!this.isRecording) return;
            const inputBuffer = event.inputBuffer.getChannelData(0);
            const bufferCopy = new Float32Array(inputBuffer);
            this.buffers.push(bufferCopy);
            this.recordingLength += bufferCopy.length;
        };

        this.source.connect(this.scriptProcessor);
        this.scriptProcessor.connect(this.audioContext.destination);
        this.isRecording = true;
    }

    async stop(): Promise<Blob> {
        this.isRecording = false;

        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
            this.mediaStream = null;
        }

        if (this.source && this.scriptProcessor) {
            this.source.disconnect();
            this.scriptProcessor.disconnect();
        }

        if (this.audioContext) {
            await this.audioContext.close();
            this.audioContext = null;
        }

        return this.exportWAV();
    }

    private exportWAV(): Blob {
        const buffer = this.mergeBuffers(this.buffers, this.recordingLength);
        const dataview = this.encodeWAV(buffer);
        return new Blob([dataview.buffer as ArrayBuffer], { type: 'audio/wav' });
    }

    private mergeBuffers(buffers: Float32Array[], validLength: number): Float32Array {
        const result = new Float32Array(validLength);
        let offset = 0;
        for (const buffer of buffers) {
            result.set(buffer, offset);
            offset += buffer.length;
        }
        return result;
    }

    private encodeWAV(samples: Float32Array): DataView {
        const buffer = new ArrayBuffer(44 + samples.length * 2);
        const view = new DataView(buffer);

        // RIFF chunk descriptor
        this.writeString(view, 0, 'RIFF');
        view.setUint32(4, 36 + samples.length * 2, true);
        this.writeString(view, 8, 'WAVE');

        // fmt sub-chunk
        this.writeString(view, 12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true); // PCM (linear quantization)
        view.setUint16(22, 1, true); // Mono (1 channel)
        view.setUint32(24, this.sampleRate, true);
        view.setUint32(28, this.sampleRate * 2, true);
        view.setUint16(32, 2, true); // Block align
        view.setUint16(34, 16, true); // Bits per sample

        // data sub-chunk
        this.writeString(view, 36, 'data');
        view.setUint32(40, samples.length * 2, true);

        // Write the PCM samples
        this.floatTo16BitPCM(view, 44, samples);

        return view;
    }

    private floatTo16BitPCM(output: DataView, offset: number, input: Float32Array): void {
        for (let i = 0; i < input.length; i++, offset += 2) {
            const s = Math.max(-1, Math.min(1, input[i]));
            output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
        }
    }

    private writeString(view: DataView, offset: number, string: string): void {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }
}
