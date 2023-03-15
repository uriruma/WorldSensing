import React, { useState, useEffect } from 'react'
import '../styles/api-control-panel.css'
import axios from 'axios';

function Api() {
    // React Hooks we will use to manage the requests
    const [sortMaps, setSortMaps] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/sortmaps')
          .then(response => {
            setSortMaps(response.data.sortmaps);
            console.log(response.data); 
          })
          .catch(error => {
            console.error(error);
          });
      }, []);
    
    return (
        <div className="api-control-panel">
            <h2 className="api-title">API Control Panel</h2>
            <div className="api-data-card">
            <h1 className="api-subtitle">Data from API</h1>
            <table className="api-data-table">
                <thead>
                    <tr>
                        <th>SortMap ID</th>
                        <th>SortMap Value</th>
                    </tr>
                </thead>
                <tbody>
                    {sortMaps.map((sortMap) => (
                    <tr key={sortMap.id}>
                        <td>{sortMap.id}</td>
                        <td>{sortMap.value}</td>
                    </tr>
            ))}
      </tbody>
    </table>
  </div>
</div>


    );
}

export default Api;
