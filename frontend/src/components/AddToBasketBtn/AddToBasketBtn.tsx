import React, { useState } from 'react';
import api from '../../services/api';
import { getToken } from '../../services/auth';

export interface AddToBasketBtnProps {
    productId: number;
}

export const AddToBasketBtn: React.FC<AddToBasketBtnProps> = ({ productId }) => {
    const [quantity, setQuantity] = useState<number>(1);

    const handleQuantityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = parseInt(event.target.value, 10);
        if (!isNaN(value) && value > 0) {
            setQuantity(value);
        }
    };

    const handleAddToBasket = async () => {
        try {
            await api.post('/basket/add', {
                product_id: productId,
                quantity: quantity
            }, {
                headers: {
                    Authorization: `Bearer ${getToken()}`
                }
            });

            alert(`Added ${quantity}x product (ID: ${productId}) to the basket.`);
        } catch (error) {
            alert('Failed to add the product to the basket.');
            console.error(error);
        }
    };

    return (
        <>
            <input
                type="number"
                value={quantity}
                onChange={handleQuantityChange}
                placeholder="0"
                min={1}
                style={{ width: 36, marginRight: 2 }}
            />
            <button type="button" onClick={handleAddToBasket}>
                Add
            </button>
        </>
    );
};
