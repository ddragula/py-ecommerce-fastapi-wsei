import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { getToken } from '../services/auth';

export interface Product {
    id: number;
    name: string;
    description: string;
    price: number;
}

export interface BasketItem {
    product: Product;
    quantity: number;
}

export interface BasketData {
    id: number;
    items: BasketItem[];
}

export const Basket: React.FC = () => {
    const [basket, setBasket] = useState<BasketData | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchBasket = async () => {
            setLoading(true);
            setError(null);

            try {
                const token = getToken();
                if (!token) {
                    setError('User not authenticated.');
                    setLoading(false);
                    return;
                }

                const response = await api.get('/basket/', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                setBasket(response.data);
            } catch (err) {
                setError('Error: ' + (err as Error).message);
            } finally {
                setLoading(false);
            }
        };

        fetchBasket();
    }, []);

    const handleOrder = async () => {
        try {
            const token = getToken();
            if (!token) {
                alert('User not authenticated.');
                return;
            }

            await api.post(
                '/orders/place',
                {}, // Empty body as required
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            alert('Order placed successfully!');
            setBasket(null); // Clear basket after ordering
        } catch (error) {
            alert('Failed to place order.');
            console.error(error);
        }
    };

    return (
        <div className="Basket-container">
            <h1>Your Basket</h1>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && basket && basket.items.length > 0 ? (
                <table className="styled-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Price</th>
                            <th>Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
                        {basket.items.map((item) => (
                            <tr key={item.product.id}>
                                <td>{item.product.id}</td>
                                <td>{item.product.name}</td>
                                <td>{item.product.description}</td>
                                <td>{item.product.price} zł</td>
                                <td>{item.quantity}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>Your basket is empty.</p>
            )}

            {basket && basket.items.length > 0 && (
                <button onClick={handleOrder} style={{ marginTop: '10px' }}>
                    Order
                </button>
            )}
        </div>
    );
};
