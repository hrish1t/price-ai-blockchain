import React from "react";

function ResultCard({ result }) {

  if (!result) return null;

  const riskColor =
    result.risk === "HIGH"
      ? "bg-red-600"
      : result.risk === "MEDIUM"
      ? "bg-yellow-500"
      : "bg-green-600";

  return (
    <div className="mt-8 grid grid-cols-3 gap-6">

      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="text-lg text-gray-600">Predicted Price</h2>
        <p className="text-2xl font-bold">
          ₹{result.predicted_price}
        </p>
      </div>

      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="text-lg text-gray-600">% Change</h2>
        <p className="text-2xl font-bold">
          {result.percent_change}%
        </p>
      </div>

      <div className={`${riskColor} p-6 rounded-xl shadow text-white`}>
        <h2 className="text-lg">Risk Level</h2>
        <p className="text-2xl font-bold">
          {result.risk}
        </p>
      </div>

      <div className="col-span-3 bg-white p-6 rounded-xl shadow mt-4">
        <h3 className="font-semibold">Blockchain Proof</h3>
        <p className="text-sm break-all">
          Hash: {result.blockchain_hash}
        </p>
        <a
          href={`https://sepolia.etherscan.io/tx/${result.transaction_hash}`}
          target="_blank"
          rel="noreferrer"
          className="text-blue-600 underline"
        >
          View Transaction on Etherscan
        </a>
      </div>

    </div>
  );
}

export default ResultCard;
