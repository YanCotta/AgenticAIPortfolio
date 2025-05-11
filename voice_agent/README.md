# Voice Agent System

## Overview
A sophisticated voice-enabled AI agent system leveraging state-of-the-art Speech-to-Text (STT), Text-to-Speech (TTS), and Language Model technologies. This system demonstrates advanced agent capabilities with real-time voice interaction, performance monitoring, and latency optimization.

## Key Features
- Real-time voice interaction using LiveKit Agents
- Multiple voice personality options via ElevenLabs
- Performance metrics tracking and optimization
- Voice activity detection using Silero VAD
- Multi-language support with automatic language detection
- Low-latency response system

## Technical Stack
- LiveKit Agents Framework
- OpenAI GPT-4 & Whisper API
- ElevenLabs Text-to-Speech
- Silero Voice Activity Detection
- FastAPI & Uvicorn
- Python 3.10+

## Components
The project consists of two main notebooks:

### 1. Voice Agent Components (`voice_agent_components.ipynb`)
- Core agent implementation
- Voice personality customization
- Language detection
- Interactive voice communication setup

### 2. Latency Optimization (`optimizing_latency.ipynb`)
- Performance metrics collection and analysis
- Latency monitoring for:
  - LLM response time
  - Speech-to-Text processing
  - Text-to-Speech generation
  - End-of-Utterance detection
- Real-time performance visualization

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```env
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```

3. Run the notebooks in a Jupyter environment

## Performance Metrics
The system tracks multiple performance indicators:
- LLM Metrics:
  - Token processing speed
  - Time to First Token (TTFT)
  - Token counts
- STT Metrics:
  - Processing duration
  - Audio duration analysis
  - Streaming performance
- TTS Metrics:
  - Time to First Byte (TTFB)
  - Audio generation speed
  - Streaming efficiency
- End of Utterance Metrics:
  - Detection delay
  - Transcription latency

## Available Voices
Pre-configured voice options:
- Roger (ID: CwhRBWXzGAHq8TQ4Fs17)
- Sarah (ID: EXAVITQu4vr4xnSDxMaL)
- Laura (ID: FGY2WhTYpPnrIDTdsKH5)
- George (ID: JBFqnCBsd6RMkjVDRZzb)

## Future Enhancements
- Custom voice training integration
- Advanced conversation memory
- Emotion detection
- Multi-agent voice conversations
- Voice style transfer capabilities
