import React from "react";
import { getLogsAction } from "../../actions/actions";
import { PopulatedLog, Severity } from "../../lib/models";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faUserTie } from "@fortawesome/free-solid-svg-icons";

const AdminLogs = async () => {
  const logs: PopulatedLog[] = await getLogsAction();

  const showRoleIcon = (log: PopulatedLog) => {
    return (
      <abbr title={log.roleId.name.charAt(0).toUpperCase() + log.roleId.name.slice(1)}>
        <FontAwesomeIcon className="mr-1 hover:scale-125 transition-transform" icon={log.roleId.name !== "user" ? faUserTie : faUser} color="white" width={30} height={30} />
      </abbr>
    )
  };

  if (logs.length === 0) {
    return (
      <h2 className="text-center font-bold text-2xl text-white font-sans">
        No logs found
      </h2>
    );
  }

  return (
    <table className="w-full">
      <thead>
        <tr>
          <th className="table-header">User</th>
          <th className="table-header">Date</th>
          <th className="table-header">Action</th>
          <th className="table-header">Severity</th>
          <th className="table-header">Description</th>
        </tr>
      </thead>
      <tbody className="bg-[#292438] text-center text-lg text-white">
        {logs.map((log) => (
          <tr className="border-2 border-table-border" key={log._id?.toString()}>
            <td className="flex p-2 flex-wrap">
              {showRoleIcon(log)}
              {log.userId?.username || "Unknown"}
            </td>
            <td className="p-2">{new Date(log.createdAt).toLocaleString()}</td>
            <td className="p-2">{log.action}</td>
            <td className={`p-2 ${log.severity === Severity.LOW ? "bg-blue-400/40" : log.severity === Severity.MEDIUM ? "bg-yellow-400/40" : "bg-red-400/40"}`}>{log.severity}</td>
            <td className="p-2">{log.description}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default AdminLogs;
