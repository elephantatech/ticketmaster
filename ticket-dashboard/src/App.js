import React, { useEffect, useState } from "react";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import 'chart.js/auto';  // Import Chart.js

function App() {
    const [tickets, setTickets] = useState([]);
    const [filteredTickets, setFilteredTickets] = useState([]);
    const [summary, setSummary] = useState({});

    useEffect(() => {
        fetchTickets();
    }, []);

    const fetchTickets = async () => {
        try {
            // Adjust the URL to point to your existing API endpoint
            const response = await axios.get("http://backend:8000/api/tickets");
            const allTickets = response.data;

            // Filter tickets to include only today's tickets, excluding "complete" and "resolved"
            const today = new Date().toISOString().split('T')[0];
            const todayTickets = allTickets.filter(ticket => {
                const ticketDate = new Date(ticket.created_date).toISOString().split('T')[0];
                return ticketDate === today && !["complete", "resolved"].includes(ticket.status.toLowerCase());
            });

            setFilteredTickets(todayTickets);

            // Group tickets by status for the summary
            const statusSummary = todayTickets.reduce((acc, ticket) => {
                acc[ticket.status] = (acc[ticket.status] || 0) + 1;
                return acc;
            }, {});

            setSummary(statusSummary);

        } catch (error) {
            console.error("Error fetching tickets:", error);
        }
    };

    const chartData = {
        labels: Object.keys(summary),
        datasets: [
            {
                data: Object.values(summary),
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
            },
        ],
    };

    return (
        <div>
            <h2>Today's Tickets</h2>
            <div className="ticket-sections">
                {Object.entries(filteredTickets.reduce((acc, ticket) => {
                    acc[ticket.status] = acc[ticket.status] || [];
                    acc[ticket.status].push(ticket);
                    return acc;
                }, {})).map(([status, tickets]) => (
                    <div key={status} className="ticket-section">
                        <h3>{status}</h3>
                        <ul>
                            {tickets.map(ticket => (
                                <li key={ticket.id}>{ticket.title}</li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
            <h2>Summary Chart</h2>
            <Pie data={chartData} />
        </div>
    );
}

export default App;
