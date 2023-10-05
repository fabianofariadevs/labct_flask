document.addEventListener("DOMContentLoaded", function () {

    // função para abrir o modal
    function abrirModal() {
        var modal = document.getElementById("btn-adicionarProdutoModal"); // Corrigir o nome do modal
        modal.classList.add("show");
        modal.style.display = "block";
    }

    // Função para fechar o modal
    function fecharModal() {
        var modal = document.getElementById("adicionarProdutoModal"); // Corrigir o nome do modal
        modal.classList.remove("show");
        modal.style.display = "none";
    }

    // ...

    // Event listener para o botão "Adicionar produto"
    document.querySelector("#adicionar-produto").addEventListener("click", adicionarProduto);

    // Event listener para o botão "Remover"
    document.querySelector("#remover-produto").addEventListener("click", removerProduto);

    // ...

    // Processar resposta do modal
    document.getElementById("form-adicionar-produto").addEventListener("submit", function (e) { // Corrigir o ID do formulário
        e.preventDefault();
        var formData = new FormData(this);
        fetch("/receitas/adicionar_produto_sessao", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualize a tabela de produtos e quantidades
                var tabela = document.querySelector("#tabela-produtos-quantidades tbody");
                var linha = document.createElement("tr");
                linha.innerHTML = `
                    <td>${formData.get("produtos")}</td>
                    <td>${formData.get("quantidades")}</td>
                    <td><button type="button" class="btn btn-sm btn-danger remover-produto">Remover</button></td>
                `;
                tabela.appendChild(linha);

                fecharModal(); // Fechar o modal após adicionar com sucesso

            } else {
                // Exiba mensagem de erro de forma amigável na página
                alert("Erro ao adicionar produto: " + data.error);
            }
        })
        .catch(error => console.error("Erro:", error));

    });

    // ...

    // Remover produto da lista de produtos da receita quando o botão "Remover" é clicado
    document.getElementById("tabela-produtos-quantidades").addEventListener("click", function (e) {
        if (e.target && e.target.classList.contains("remover-produto")) {
            var row = e.target.closest("tr");
            row.remove();
        }
    });

    // ...

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
                produtos: produtoId,
                quantidades: quantidade
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

    // ...

    // Limpar o formulário quando o modal é fechado
    document.getElementById("adicionarProdutoModal").addEventListener("hidden.bs.modal", function () {
        document.getElementById("form-adicionar-produto").reset();
        fecharModalError();
    });
});
