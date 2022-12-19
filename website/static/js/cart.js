(() => {
    "strict";

    const produto = (() => {
        const produtoScript = document.getElementById("produto-data");
        if (!produtoScript)
            return;
        return JSON.parse(produtoScript.innerHTML);
    })();

    const estoque = document.querySelector("#carrinho");

    function $addItem(cart, id, name, image, price, qnt, url) {
        cart.produtos[id] = { name, image, amount: qnt, price, url };

        if (produto && produto.sku in cart.produtos)
            estoque.innerHTML = qnt;
    }

    function getItem(id) {
        return openTransaction((cart) => id in cart.produtos ? cart.produtos[id] : null);
    }

    function addItem(id, name, image, price, qnt, url) {
        openTransaction((cart) => $addItem(cart, id, name, image, price, qnt, url));
    }

    function removeItem(id) {
        openTransaction((cart) => cart.produtos[id] && delete cart.produtos[id]);
    }

    async function openTransaction(func) {
        var cart = JSON.parse(localStorage.getItem("cart")) ?? { produtos: {} };
        if (cart == null || !'produtos' in cart) cart = { produtos: {} };
        rs = await func(cart);
        localStorage.setItem("cart", JSON.stringify(cart));
        return rs;
    }

    if (!produto)
        return;

    const btn = document.querySelector(".btn-cart");

    if (btn) {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            const qnt = parseInt(document.querySelector("#quantidade").value);

            openTransaction(async (cart) => {
                let { sku: id, name, imagem, offers: { price, url } } = produto;

                const noCarrinho = await getItem(id);

                if (noCarrinho) {
                    return Swal.fire({
                        title: "Produto já adicionado",
                        text: "Você já adicionou esse produto ao carrinho, deseja adicionar mais uma unidade?\nAtualmente você tem " + cart.produtos[id].amount + " unidades desse produto no carrinho.",
                        icon: "question",
                        showCancelButton: true,
                        confirmButtonText: "Sim",
                        cancelButtonText: "Não",
                        color: "#fff",
                        background: "#323232",
                    }).then((result) => {
                        if (result.isConfirmed) {
                            $addItem(cart, id, name, imagem, price, noCarrinho.amount + qnt, url);

                            Swal.fire({
                                title: "Produto adicionado",
                                text: "Produto adicionado com sucesso!",
                                icon: "success",
                                color: "#fff",
                                background: "#323232",
                            });
                        }
                    });
                } else {
                    $addItem(cart, id, name, imagem, price, qnt, url);
                }
            });
        });
    }

    if (estoque && produto) {
        openTransaction((cart) => {
            if (produto.sku in cart.produtos) {
                estoque.innerHTML = cart.produtos[produto.sku].amount;
            }
        });
    }

})();