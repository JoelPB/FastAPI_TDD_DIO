from datetime import datetime
from typing import List

import pytest
from unittest.mock import patch
from tests.factories import product_data
from fastapi import status
from store.core.exceptions import BaseException, NotFoundExcepition


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


async def test_controller_create_should_handle_insertion_exception(
    client, products_url
):
    with patch(
        "store.usecases.product.ProductUsecase.create",
        side_effect=BaseException("Simulated insertion error"),
    ):
        response = await client.post(products_url, json=product_data())

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"detail": "Simulated insertion error"}


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    # Recuperar o valor atual de updated_at antes da atualização
    response = await client.get(f"{products_url}{product_inserted.id}")
    initial_content = response.json()
    initial_updated_at = initial_content["updated_at"]

    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content["id"] == str(product_inserted.id)
    assert content["name"] == "Iphone 14 Pro Max"
    assert content["quantity"] == 10
    assert content["price"] == "7.500"
    assert content["status"] is True

    # Verifica se a data de updated_at foi alterada
    assert "updated_at" in content
    assert content["updated_at"] != initial_updated_at
    assert datetime.fromisoformat(content["updated_at"]) > datetime.fromisoformat(
        initial_updated_at
    )


async def test_controller_patch_should_return_not_found(client, products_url):
    with patch(
        "store.usecases.product.ProductUsecase.update",
        side_effect=NotFoundExcepition("Product not found"),
    ):
        response = await client.patch(
            f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca",
            json={"price": "7.500"},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Product not found"}


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }
