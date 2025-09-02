document.addEventListener('DOMContentLoaded', function() {
    const btlSelect = document.getElementById('btl_select');
    const cpaInput = document.getElementById('cpa_input');
    

    function preencherCampos() {
        const selectedOption = btlSelect.options[btlSelect.selectedIndex];

        if (selectedOption.value) { // Verifica se um btl válido foi selecionado (não a opção padrão "-- Selecione...")
            const Btl = selectedOption.textContent.trim(); // Pega o texto visível da opção
            const cpa = selectedOption.getAttribute('data-cpa');
            // btlSelect.value = Btl;
            cpaInput.value = cpa;
           
        } else {
            // Limpa os campos se a opção padrão for selecionada
            btlSelect.value = '';
            cpaInput.value = '';
        }
    }

    // Adiciona o 'listener' para o evento 'change' no select
    btlSelect.addEventListener('change', preencherCampos);

    // Chama a função uma vez ao carregar a página
    //preencherCampos();


    const btnEditar = document.getElementById('btnEditar');
    const btnSalvar = document.getElementById('btnSalvar');
    const btnCancelar = document.getElementById('btnCancelar');
    const form = document.querySelector('form');
    const campos = form.querySelectorAll('input, select, textarea');

    if (btnEditar){ // Verifica se o botão editar existe
        btnEditar.addEventListener('click', function() {
            campos.forEach(campo => {
                campo.disabled = false;
            })
            btnEditar.setAttribute('hidden', true);
            btnSalvar.removeAttribute('hidden');
            btnCancelar.removeAttribute('hidden');
        })

        btnCancelar.addEventListener('click', function() {
            campos.forEach(campo => {
                campo.disabled = true;
            })
            btnEditar.removeAttribute('hidden');
            btnSalvar.setAttribute('hidden', true);
            btnCancelar.setAttribute('hidden', true);
        })
    
        


    }
});