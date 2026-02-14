import React, { useState } from "react";
import { predictPrice } from "../services/api";

function InputForm({ setResult }) {

  const [formData, setFormData] = useState({
    lag_1: "",
    lag_7: "",
    ma_7: "",
    rainfall: "",
    temperature: "",
    month: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value)
    });
  };

  const handleSubmit = async () => {
    const result = await predictPrice(formData);
    setResult(result);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md grid grid-cols-2 gap-4">
      {Object.keys(formData).map((key) => (
        <div key={key}>
          <label className="block text-sm font-medium text-gray-700">
            {key}
          </label>
          <input
            type="number"
            name={key}
            onChange={handleChange}
            className="mt-1 w-full border rounded-md p-2"
          />
        </div>
      ))}

      <button
        onClick={handleSubmit}
        className="col-span-2 mt-4 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
      >
        Predict Price
      </button>
    </div>
  );
}

export default InputForm;
