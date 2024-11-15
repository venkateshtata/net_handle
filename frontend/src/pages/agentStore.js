import { useState } from "react";
import AgentCard from "../components/agentCard.js";

const AgentStore = () => {

    const [searchTerm, setSearchTerm] = useState("");
    const cards = [
        { id: 1, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card One", description: "This is the first card." },
        { id: 2, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Two", description: "This is the second card." },
        { id: 3, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Three", description: "This is the third card." },
        { id: 4, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Four", description: "This is the fourth card." },
        { id: 5, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 6, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 7, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 8, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 9, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 10, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 11, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card One", description: "This is the first card." },
        { id: 12, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Two", description: "This is the second card." },
        { id: 13, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Three", description: "This is the third card." },
        { id: 14, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Four", description: "This is the fourth card." },
        { id: 15, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 16, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 17, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 18, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 19, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 20, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 21, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card One", description: "This is the first card." },
        { id: 22, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Two", description: "This is the second card." },
        { id: 23, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Three", description: "This is the third card." },
        { id: 24, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Four", description: "This is the fourth card." },
        { id: 25, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 26, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 27, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 28, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 29, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
        { id: 30, avatar: "https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid", title: "Card Five", description: "This is the fifth card." },
    ];
  
    const filteredCards = cards.filter(card =>
      card.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

  return (
    <div className="min-h-full text-white p-4 grid place-items-center items-start">
      <div className="sticky top-0 mb-6 h-40 w-full flex flex-col items-center">
        <div className="bg-white min-w-full text-center">
          <h1 className="text-4xl text-black font-silkscreen">Agent Hub </h1>
        </div>
        <div className="w-full grid place-items-center backdrop-blur-xl">
          <div className="w-full grid place-items-center  bg-gradient-to-t from-transparent to-white">
            <input
              type="text"
              className="mt-10 w-1/4 pl-6 py-2 rounded-full bg-black opacity-80 hover:shadow-2xl-dark text-white placeholder-gray-500 focus:outline-none transition duration:700"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-20">
        {filteredCards.map(card => (
          <div
            key={card.id}
          >
            <AgentCard avatar={card.avatar} title={card.title} description={card.description} />  
          </div>
        ))}
        {filteredCards.length === 0 && (
          <div className="col-span-full text-center text-gray-500">
            No results found.
          </div>
        )}
      </div>
    </div>
  )
}

export default AgentStore;