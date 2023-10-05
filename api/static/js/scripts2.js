document.addEventListener("DOMContentLoaded", function () {
    // Abrir modal de adicionar produto
    document.getElementById("btn-adicionar-produto").addEventListener("click", function () {
        document.getElementById("adicionarProdutoModal").classList.add("show");
        document.getElementById("adicionarProdutoModal").style.display = "block";

        // Carregar lista de produtos
        fetch("/produtos/listar")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var select = document.getElementById("produto_id");
                data.produtos.forEach(function (produto) {
                    var option = document.createElement("option");
                    option.value = produto.id;
                    option.text = produto.nome;
                    select.appendChild(option);
                });
            } else {
                alert("Erro ao carregar lista de produtos: " + data.error);
            }
        })
        .catch(error => console.error("Erro:", error));
    });

    // Fechar modal de adicionar produto
    document.getElementById("fechar-modal").addEventListener("click", function () {
        document.getElementById("adicionarProdutoModal").classList.remove("show");
        document.getElementById("adicionarProdutoModal").style.display = "none";
    });

    // Processar resposta do modal
    document.querySelector("form-adicionar-produto").addEventListener("submit", function (e) {
        e.preventDefault();
        var formData = new FormData(this);
        fetch("/receitas/adicionar_produto", {
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
                        <td>${formData.get("produto_id")}</td>
                        <td>${formData.get("quantidade")}</td>
                        <td><button type="button" class="btn btn-sm btn-danger remover-produto">Remover</button></td>
                    `;
                    tabela.appendChild(linha);

                    // Feche o modal
                    document.getElementById("adicionarProdutoModal").classList.remove("show");
                    document.getElementById("adicionarProdutoModal").style.display = "none";
                } else {
                    alert("Erro ao adicionar produto: " + data.error);
                }
            })
            .catch(error => console.error("Erro:", error));
        });
    }

    // Código JavaScript a ser executado após o carregamento completo do DOM
    // Adicionar produto à lista de produtos da receita quando o botão "Adicionar" é clicado
    document.getElementById("adicionar-produto").addEventListener("click", function () {
    document.getElementById("adicionarProdutoModal").classList.add("show");
    document.getElementById("adicionarProdutoModal").style.display = "block";
        if document.getElementById("form-adicionar-produto").checkValidity()) {
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

    // Remover produto da lista de produtos da receita quando o botão "Remover" é clicado
    document.getElementById("tabela-produtos-quantidades").addEventListener("click", function (e) {
        if (e.target.classList.contains("remover-produto")) {
            e.target.parentElement.parentElement.remove();
        }
    });

    // Processar formulário de adicionar produto
    document.getElementById("form-adicionar-produto").addEventListener("submit", function (e) {
        e.preventDefault();
        var formData = new FormData(this);
        fetch("/receitas/adicionar_produto", {
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
                    <td>${formData.get("produto_id")}</td>
                    <td>${formData.get("quantidade")}</td>
                    <td><button type="button" class="btn btn-sm btn-danger remover-produto">Remover</button></td>
                `;
                tabela.appendChild(linha);

                // Feche o modal
                document.getElementById("adicionarProdutoModal").classList.remove("show");
                document.getElementById("adicionarProdutoModal").style.display = "none";
            } else {
                alert("Erro ao adicionar produto: " + data.error);
            }
        })
        .catch(error => console.error("Erro:", error));
    }

    // Processar formulário de adicionar receita
    document.getElementById("form-adicionar-receita").addEventListener("submit", function (e) {
        e.preventDefault();
        var formData = new FormData(this);
        fetch("/receitas/adicionar", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirecionar para a página da receita
                window.location.href = "/receitas/" + data.receita_id;
            } else {
                alert("Erro ao adicionar receita: " + data.error);
            }
        })
        .catch(error => console.error("Erro:", error));
    }

    // Processar formulário de editar receita
    document.getElementById("form-editar-receita").addEventListener("submit", function (e) {
        e.preventDefault();
        var formData = new FormData(this);
        fetch("/receitas/editar", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirecionar para a página da receita
                window.location.href = "/receitas/" + data.receita_id;
            } else {
                alert("Erro ao editar receita: " + data.error);
            }
        })
        .catch(error => console.error("Erro:", error));
    }

});
