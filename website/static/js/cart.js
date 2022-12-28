(() => {
    "strict";

    /*
        Endpoints para o carrinho:
        - api/carrinho/remover (POST) - Remove um item do carrinho {produto_id}
        - api/carrinho/adicionar (POST) - Adiciona um item ao carrinho {produto_id, quantidade}
        - api/carrinho/limpar (POST) - Limpa o carrinho
    */

    function clickAction(e, el, action) {
        e.preventDefault();
        el.setAttribute("disabled", true);
        action().finally(() => el.removeAttribute("disabled"));
    }


    function defineValue(value) {
        if ((a = document.getElementById("carrinho-contador"))) {
            a.innerHTML = value;
        }
    }

    async function tratar(res) {
        if (res.status === 401) {
            Swal.fire({
                title: "Erro",
                text: "Você precisa estar logado para adicionar um produto ao carrinho!",
                icon: "error",
                color: "#fff",
                background: "#323232",
            });
        } else {
            try {
                const json = await res.json();
                Swal.fire({
                    title: "Erro",
                    text: Object.values(json).join("\n"),
                    icon: "error",
                    color: "#fff",
                    background: "#323232",
                });
            } catch (e) {
                Swal.fire({
                    title: "Erro",
                    text: "Ocorreu um erro ao adicionar o produto ao carrinho!",
                    icon: "error",
                    color: "#fff",
                    background: "#323232",
                });
            }
        }
    }

    function data() {
        return [...new FormData(document.getElementById("csfr"))].reduce((acc, [key, value]) => {
            acc[key] = value;
            return acc;
        }, {});
    }

    if (form = document.getElementById("csfr")) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
        });
    }

    async function makeRequest(method, body) {
        return fetch(`/api/carrinho/${method}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
                'X-CSRFToken': data()['csrfmiddlewaretoken']
            },
            credentials: "include",
            ...(body && { body: JSON.stringify(body) }),
        })
    }

    async function addItem(id, qnt, force = false) {
        return makeRequest("add", { id, quantidade: qnt, force }).then(async (res) => {
            if (res.status === 200) {
                rs = await res.json();
                if (rs.status === 'success') {
                    Swal.fire({
                        title: "Produto adicionado",
                        text: "Produto adicionado com sucesso!",
                        icon: "success",
                        color: "#fff",
                        background: "#323232",
                    });
                    defineValue(rs.quantidade);
                } else {
                    Swal.fire({
                        title: "Produto já adicionado",
                        text: "Você já adicionou esse produto ao carrinho, deseja adicionar mais uma unidade?\nAtualmente você tem " + rs['quantidade'] + " unidades desse produto no carrinho.",
                        icon: "question",
                        showCancelButton: true,
                        confirmButtonText: "Sim",
                        cancelButtonText: "Não",
                        color: "#fff",
                        background: "#323232",
                    }).then(async (result) => {
                        if (result.isConfirmed) {
                            await addItem(id, qnt, true);
                        }
                    });
                }
            } else {
                await tratar(res);
            }
        });
    }

    async function removeItem(id) {
        return fetch("/api/carrinho/rem", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': data()['csrfmiddlewaretoken']
            },
            credentials: "include",
            body: JSON.stringify({
                id: id,
            })
        }).then(async (res) => {
            if (res.status === 200) {
                rs = await res.json();
                if (rs.status === 'success') {
                    await Swal.fire({
                        title: "Produto removido",
                        text: "Produto removido com sucesso!",
                        icon: "success",
                        color: "#fff",
                        background: "#323232",
                    });
                    defineValue(rs.quantidade);
                } else {
                    await Swal.fire({
                        title: "Error",
                        text: "Produto já foi removido ou não existe!",
                        icon: "error",
                        color: "#fff",
                        background: "#323232",
                    });
                }
            } else {
                await tratar(res);
                return false;
            }
            return true;
        });
    }

    async function clearCart() {
        return fetch("/api/carrinho/clear", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': data()['csrfmiddlewaretoken']
            },
            credentials: "include"
        }).then(async (res) => {
            if (res.status === 200) {
                rs = await res.json();
                if (rs.status === 'success') {
                    Swal.fire({
                        title: "Carrinho limpo",
                        text: "Carrinho limpo com sucesso!",
                        icon: "success",
                        color: "#fff",
                        background: "#323232",
                    });
                    defineValue(0);
                } else {
                    Swal.fire({
                        title: "Error",
                        text: "Carrinho já está vazio!",
                        icon: "error",
                        color: "#fff",
                        background: "#323232",
                    });
                }
            } else {
                await tratar(res);
                return false;
            }
            return true;
        });
    }

    if ((btn = document.getElementById("cart-clear"))) {
        btn.addEventListener("click", (e) => clickAction(e, btn, () => clearCart()));
    }

    for (let btnRemove of document.getElementsByClassName("remover-produto")) {
        btnRemove.addEventListener("click", (e) => clickAction(e, btnRemove, async () => {
            const elemento = await removeItem(btnRemove.dataset.id);
            if (elemento && btnRemove.dataset.redirect) {
                window.location.href = window.location.href;
            }
        }));
    }

    if ((btn = document.getElementById("cart-add"))) {
        const produto = (() => {
            const produtoScript = document.getElementById("produto-data");
            if (!produtoScript)
                return;
            return JSON.parse(produtoScript.innerHTML);
        })();
        if (!produto)
            return;
        btn.addEventListener("click", e => clickAction(e, btn, () => addItem(produto.sku, parseInt(document.getElementById("produto-qnt").value))));
    }


})();