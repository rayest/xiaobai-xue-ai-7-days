import test from 'node:test';
import assert from 'node:assert/strict';
import { createFlightAudio } from './audio.js';

test('engine responds to speed, pauses to silence, and supports mute', () => {
  const gains = [], oscillators = [];
  const parameter = () => ({ value: 0, setTargetAtTime(value) { this.value = value; } });
  const node = () => ({ connect() {}, start() {} });
  const previous = globalThis.AudioContext;
  globalThis.AudioContext = class {
    currentTime = 0; sampleRate = 100; destination = {};
    resume() { return Promise.resolve(); }
    createGain() { const result = { ...node(), gain: parameter() }; gains.push(result); return result; }
    createOscillator() { const result = { ...node(), frequency: parameter() }; oscillators.push(result); return result; }
    createBuffer() { return { getChannelData: () => new Float32Array(200) }; }
    createBufferSource() { return node(); }
    createBiquadFilter() { return { ...node(), frequency: parameter() }; }
  };
  try {
    const audio = createFlightAudio(); audio.unlock(); audio.update(true, 18, 0);
    const cruisePitch = oscillators[0].frequency.value;
    assert.ok(gains[1].gain.value > 0);
    audio.update(true, 40.5, 1);
    assert.ok(oscillators[0].frequency.value > cruisePitch);
    audio.update(false, 18, 0);
    assert.equal(gains[1].gain.value, 0); assert.equal(gains[2].gain.value, 0);
    audio.setEnabled(false); assert.equal(gains[0].gain.value, 0);
    audio.setEnabled(true); assert.ok(gains[0].gain.value > 0);
  } finally { globalThis.AudioContext = previous; }
});
