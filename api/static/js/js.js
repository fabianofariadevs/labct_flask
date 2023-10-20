document.addEventListener('DOMContentLoaded', function () {
    // Abrir modal de adicionar produto
    document.getElementById('btn-adicionar-produto').addEventListener('click', function () {
        document.getElementById('modal-adicionar-produto').style.display = 'block';
    });

    // Fechar modal de adicionar produto
    document.getElementById('fechar-modal').addEventListener('click', function () {
        document.getElementById('modal-adicionar-produto').style.display = 'none';
    });

    // Processar resposta do modal
    document.querySelector('form#modal-adicionar-produto').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        fetch('/receitas/adicionar_produto', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualize a tabela de produtos e quantidades
                const tabela = document.querySelector('#tabela-produtos-quantidades tbody');
                const linha = document.createElement('tr');
                linha.innerHTML = `
                    <td>${formData.get('produto_id')}</td>
                    <td>${formData.get('quantidade')}</td>
                `;
                tabela.appendChild(linha);

                // Feche o modal
                document.getElementById('modal-adicionar-produto').style.display = 'none';
            } else {
                alert('Erro ao adicionar produto: ' + data.error);
            }
        })
        .catch(error => console.error('Erro:', error));
    });

        // Código JavaScript a ser executado após o carregamento completo do DOM
    // Adicionar produto à lista de produtos da receita quando o botão "Adicionar" é clicado
    document.getElementById("adicionar-produto").addEventListener("click", function () {
        // Validar e processar o formulário
        if (document.getElementById("form-adicionar-produto").checkValidity()) {
            var produtoId = int(document.getElementById("produto_id").value);
            var quantidade = document.getElementById("quantidade").value;

            // Verificar se a quantidade é maior que zero
            if (quantidade <= 0) {
                alert("A quantidade deve ser maior que zero.");
                return;
            }

            // Verificar se o produto já está na lista de produtos da receita
            var produtoJaAdicionado = false;
            var tabelaProdutosQuantidades = document.getElementById("tabela-produtos-quantidades");
            for (var i = 0; i < tabelaProdutosQuantidades.rows.length; i++) {
                var idExistente = tabelaProdutosQuantidades.rows[i].cells[0].textContent;
                if (idExistente === produtoId) {
                    produtoJaAdicionado = true;
                    break;
                }
            }

            if (produtoJaAdicionado) {
                alert("Este produto já foi adicionado à receita.");
                return;
            }

            // Adicionar à tabela de produtos da receita
            var newRow = tabelaProdutosQuantidades.insertRow();
            var cell1 = newRow.insertCell(0);
            var cell2 = newRow.insertCell(1);
            cell1.innerHTML = produtoId;
            cell2.innerHTML = quantidade;

            // Fechar o modal
            document.getElementById("adicionarProdutoModal").classList.remove("show");
            document.getElementById("adicionarProdutoModal").style.display = "none";
        }
    });

    // Remover produto da lista de produtos da receita quando o botão "Remover" é clicado
    document.getElementById("tabela-produtos-quantidades").addEventListener("click", function (e) {
        if (e.target && e.target.classList.contains("remover-produto")) {
            var row = e.target.closest("tr");
            row.remove();
        }
    });

    // Enviar a lista de produtos e quantidades para o formulário de cadastro de receita antes de salvar
    document.getElementById("form-cadastro-receita").addEventListener("submit", function (event) {
        event.preventDefault();

        // Criar um array para armazenar produtos e quantidades
        var produtosQuantidades = [];
        var tabelaProdutosQuantidades = document.getElementById("tabela-produtos-quantidades");
        for (var i = 1; i < tabelaProdutosQuantidades.rows.length; i++) {
            var produtoId = tabelaProdutosQuantidades.rows[i].cells[0].textContent;
            var quantidade = tabelaProdutosQuantidades.rows[i].cells[1].textContent;
            produtosQuantidades.push({
                produto_id: produtoId,
                quantidade: quantidade
            });
        }

        // Adicionar os dados ao campo de formulário oculto
        var produtosQuantidadesInput = document.createElement("input");
        produtosQuantidadesInput.setAttribute("type", "hidden");
        produtosQuantidadesInput.setAttribute("name", "produtos_quantidades");
        produtosQuantidadesInput.setAttribute("value", JSON.stringify(produtosQuantidades));
        this.appendChild(produtosQuantidadesInput);

        // Enviar o formulário de cadastro de receita com os dados dos produtos e quantidades
        this.submit();
    });

    // Limpar o formulário quando o modal é fechado
    document.getElementById("adicionarProdutoModal").addEventListener("hidden.bs.modal", function () {
        document.getElementById("form-adicionar-produto").reset();
    });
});


});