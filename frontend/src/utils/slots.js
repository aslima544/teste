// src/utils/slots.js

export function gerarSlots(inicio, fim, intervaloMinutos = 15) {
  const slots = [];
  let [h, m] = inicio.split(':').map(Number);
  let [hFim, mFim] = fim.split(':').map(Number);

  let data = new Date(0, 0, 0, h, m);
  const dataFim = new Date(0, 0, 0, hFim, mFim);

  while (data <= dataFim) {
    slots.push(data.toTimeString().slice(0,5));
    data.setMinutes(data.getMinutes() + intervaloMinutos);
  }
  return slots;
}