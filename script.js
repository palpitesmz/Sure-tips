let dados = {};

fetch('dados.json')
  .then(res => res.json())
  .then(data => {
    dados = data;
    carregarJogos();
  });

function openTab(tab) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(tab).classList.add('active');
  event.target.classList.add('active');
}

function carregarJogos() {
  // Grátis
  let html = '';
  dados.palpites_gratis.forEach(g => {
    html += `<div class="game-card"><strong>${g.jogo}</strong><br>${g.palpite} - Odd: ${g.odd}</div>`;
  });
  document.getElementById('gratis-games').innerHTML = html;

  // Resultados
  html = '';
  dados.resultados_ontem.forEach(r => {
    html += `<div class="game-card">${r.jogo} - ${r.resultado} <strong>${r.status}</strong></div>`;
  });
  document.getElementById('gratis-results').innerHTML = html;
}

function unlock(tipo) {
  let senhaDigitada = document.getElementById('senha-' + tipo).value;
  let senhaCerta = tipo === 'diario' ? dados.senha_vip_diario : dados.senha_vip_semanal;
  
  if (senhaDigitada === senhaCerta) {
    document.getElementById('vip' + tipo + '-locked').style.display = 'none';
    document.getElementById('vip' + tipo + '-games').classList.remove('hidden');
    
    let lista = tipo === 'diario' ? dados.palpites_vip_diario : dados.palpites_vip_semanal;
    let html = '';
    lista.forEach(g => {
      html += `<div class="game-card"><strong>${g.jogo}</strong><br>${g.palpite} - Odd: ${g.odd}</div>`;
    });
    document.getElementById('vip' + tipo + '-games').innerHTML = html;
  } else {
    alert('Senha incorreta!');
  }
}

function toggleResults(id) {
  let el = document.getElementById(id);
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}