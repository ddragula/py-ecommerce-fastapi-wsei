import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { getToken } from '../services/auth';

export interface Order {
    id: number;
    created_at: string;
}

export const Orders: React.FC = () => {
    const [orders, setOrders] = useState<Order[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchOrders = async () => {
            setLoading(true);
            setError(null);

            try {
                const token = getToken();
                if (!token) {
                    setError('User not authenticated.');
                    setLoading(false);
                    return;
                }

                const response = await api.get('/orders/', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                setOrders(response.data);
            } catch (err) {
                setError('Error: ' + (err as Error).message);
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, []);

    const handleDownloadXML = (orderId: number) => {
        const xmlUrl = `/api/orders/${orderId}/xml`;
        window.open(xmlUrl, '_blank');
    };

    return (
        <div className="Orders-container">
            <h1>Your Orders</h1>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && orders.length > 0 ? (
                <table className="styled-table">
                    <thead>
                        <tr>
                            <th>Order ID</th>
                            <th>Created At</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {orders.map((order) => (
                            <tr key={order.id}>
                                <td>{order.id}</td>
                                <td>{new Date(order.created_at).toLocaleString()}</td>
                                <td>
                                    <button onClick={() => handleDownloadXML(order.id)}>
                                        View XML
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>You have no orders.</p>
            )}
        </div>
    );
};
