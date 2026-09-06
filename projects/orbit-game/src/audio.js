// Audio is unlocked by the first user gesture; no remote audio assets are needed.
export function createFlightAudio() {
  let context, master, engineGain, engine, airGain, filter;
  let enabled = true;
  function unlock() {
    try {
      if (!context) {
        context = new AudioContext();
        master = context.createGain(); master.gain.value = enabled ? .55 : 0; master.connect(context.destination);
        engineGain = context.createGain(); engineGain.gain.value = 0; engineGain.connect(master);
        engine = context.createOscillator(); engine.type = 'triangle'; engine.frequency.value = 65; engine.connect(engineGain); engine.start();
        const buffer = context.createBuffer(1, context.sampleRate * 2, context.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
        const air = context.createBufferSource(); air.buffer = buffer; air.loop = true;
        filter = context.createBiquadFilter(); filter.type = 'lowpass'; filter.frequency.value = 350;
        airGain = context.createGain(); airGain.gain.value = 0;
        air.connect(filter); filter.connect(airGain); airGain.connect(master); air.start();
      }
      context.resume().catch(() => {});
    } catch { /* Gameplay remains usable when audio is unavailable. */ }
  }
  function tone(frequency, duration = .12, volume = .18) {
    if (!enabled || !context) return;
    const oscillator = context.createOscillator(), gain = context.createGain();
    oscillator.type = frequency < 150 ? 'sawtooth' : 'sine';
    oscillator.frequency.setValueAtTime(frequency, context.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(Math.max(35, frequency * .55), context.currentTime + duration);
    gain.gain.setValueAtTime(volume, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(.001, context.currentTime + duration);
    oscillator.connect(gain); gain.connect(master); oscillator.start(); oscillator.stop(context.currentTime + duration);
    oscillator.onended = () => { oscillator.disconnect(); gain.disconnect(); };
  }
  return {
    unlock, tone,
    laser() { tone(1100,.075,.025); },
    explosion(boss) { tone(boss?45:85,boss?.65:.25,boss?.3:.18); },
    setEnabled(value) { enabled = value; unlock(); if (master) master.gain.setTargetAtTime(value ? .55 : 0, context.currentTime, .03); },
    update(running, speed, boost) {
      if (!context) return;
      const now = context.currentTime;
      engine.frequency.setTargetAtTime(55 + speed * 2.1, now, .12);
      engineGain.gain.setTargetAtTime(running ? .12 + boost * .08 : 0, now, .06);
      filter.frequency.setTargetAtTime(250 + speed * 12 + boost * 900, now, .12);
      airGain.gain.setTargetAtTime(running ? .12 + boost * .2 : 0, now, .06);
    },
  };
}
