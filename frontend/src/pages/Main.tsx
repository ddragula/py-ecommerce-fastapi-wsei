import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { getUsername, addLoginListener } from '../services/auth';
import { AddToBasketBtn } from '../components/AddToBasketBtn/AddToBasketBtn';

export interface Product {
    id: number;
    name: string;
    description: string;
    price: number;
}

export const MainPage: React.FC = () => {
    const limit = 10;
    const [logged, setLogged] = useState<boolean>(!!getUsername());
    const [products, setProducts] = useState<Product[]>([]);
    const [skip, setSkip] = useState<number>(0);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [hasMore, setHasMore] = useState<boolean>(true);

    useEffect(() => {
        const fetchProducts = async () => {
            setLoading(true);
            setError(null);

            try {
                const response = await api.get(`/products/?skip=${skip}&limit=${limit}`);
                const newProducts = response.data;

                setProducts(newProducts);
                setHasMore(newProducts.length === limit);
            } catch (err) {
                setError('Error: ' + (err as Error).message);
            } finally {
                setLoading(false);
            }
        };

        addLoginListener('Main', (un) => setLogged(!!un));
        fetchProducts();
    }, [skip]);

    return (
        <div className='MainPage-container'>
            <h1>Product list</h1>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && (
                <table className='styled-table'>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Price</th>
                            { logged && <th>
                                Buy
                            </th> }
                        </tr>
                    </thead>
                    <tbody>
                        {products.map(product => (
                            <tr key={product.id}>
                                <td>{product.id}</td>
                                <td>{product.name}</td>
                                <td>{product.description}</td>
                                <td>{product.price} zł</td>
                                { logged && <td>
                                    <AddToBasketBtn productId={product.id} />
                                </td> }
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            <div style={{ marginTop: '10px' }}>
                <button 
                    onClick={() => setSkip(prev => Math.max(prev - limit, 0))} 
                    disabled={skip === 0}
                >
                    Previous
                </button>
                <span> {skip + 1} - {skip + products.length} </span>
                <button 
                    onClick={() => setSkip(prev => (hasMore ? prev + limit : prev))} 
                    disabled={!hasMore}
                >
                    Next
                </button>
            </div>
        </div>
    );
};
