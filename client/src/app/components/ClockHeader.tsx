import React from "react";

const ClockHeader = () => {
  return (
    <thead>
      <tr>
        <th className="table-header">Name</th>
        <th className="table-header">Clock Time</th>
        <th className="table-header">Meeting Time</th>
        <th className="table-header">Break Time</th>
      </tr>
    </thead>
  );
};

export default ClockHeader;
