import { Fragment } from 'react';
import clsx from 'clsx';
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from '@headlessui/react';
import AgentStore from '../pages/agentStore';
import FleetChat from '../pages/fleetChat';

const navbarItems = [
  {
    name: 'My Fleet',
    page: [],
  },
  {
    name: 'Agent Hub',
    page: [],
  },
  {
    name: 'Fleet Chat',
    page: [],
  },
];

const Navbar = () => {
    return (
      <TabGroup className="py-8 flex flex-col w-screen h-screen space-y-1 space-x-20 overflow-x-hidden overflow-y-hidden">
        <div className="flex flex-row w-full h-16 px-20 items-center space-x-20">
          <img src="https://i.postimg.cc/QCJxcQyX/logo.png" alt="NetHandle" className="ml-10 mr-52 h-full w-auto self-left"></img>
          <TabList className="h-12 max-w-80 flex px-2 py-2 items-center gap-4 bg-black rounded-full opacity-80 drop-shadow-2xl hover:shadow-2xl-dark transition duration-500">
            {
              navbarItems.map(({name}) => (
                <Tab
                  key={name}
                  className="rounded-full py-1 px-3 text-sm/6 font-semibold text-white focus:outline-none data-[selected]:bg-white/10 data-[hover]:bg-white/5 data-[selected]:data-[hover]:bg-white/10 data-[focus]:outline-1 data-[focus]:outline-white"
                >
                  {name}
                </Tab>
              ))
            }
          </TabList>
        </div>
        <TabPanels className="flex w-full h-full py-10">
          <div className="mb-10 h-11/12 w-11/12 rounded-lg bg-white border shadow-inner-dark overflow-y-scroll"> {/* scrollbar-hide */}
            {/* <AgentStore /> */}
            <FleetChat />
          </div>
        </TabPanels>
      </TabGroup>
    );
}

export default Navbar;

// export default function Navbar() {
//   return (
//     <div className="flex h-screen w-full justify-center pt-24 px-4">
//       <div className="w-full max-w-md">
//         <TabGroup>
//           <TabList className="flex gap-4">
//             {categories.map(({ name }) => (
//               <Tab
//                 key={name}
//                 className="rounded-full py-1 px-3 text-sm/6 font-semibold text-white focus:outline-none data-[selected]:bg-white/10 data-[hover]:bg-white/5 data-[selected]:data-[hover]:bg-white/10 data-[focus]:outline-1 data-[focus]:outline-white"
//               >
//                 {name}
//               </Tab>
//             ))}
//           </TabList>
//           <TabPanels className="mt-3">
//             {categories.map(({ name, posts }) => (
//               <TabPanel key={name} className="rounded-xl bg-white/5 p-3">
//                 <ul>
//                   {posts.map((post) => (
//                     <li key={post.id} className="relative rounded-md p-3 text-sm/6 transition hover:bg-white/5">
//                       <a href="https://google.com" className="font-semibold text-white">
//                         <span className="absolute inset-0" />
//                         {post.title}
//                       </a>
//                       <ul className="flex gap-2 text-white/50" aria-hidden="true">
//                         <li>{post.date}</li>
//                         <li aria-hidden="true">&middot;</li>
//                         <li>{post.commentCount} comments</li>
//                         <li aria-hidden="true">&middot;</li>
//                         <li>{post.shareCount} shares</li>
//                       </ul>
//                     </li>
//                   ))}
//                 </ul>
//               </TabPanel>
//             ))}
//           </TabPanels>
//         </TabGroup>
//       </div>
//     </div>
//   )
// }

// import { Tab, TabGroup, TabList, TabPanel, TabPanels } from '@headlessui/react'

// const categories = [
//   {
//     name: 'Recent',
//     posts: [
//       {
//         id: 1,
//         title: 'Does drinking coffee make you smarter?',
//         date: '5h ago',
//         commentCount: 5,
//         shareCount: 2,
//       },
//       {
//         id: 2,
//         title: "So you've bought coffee... now what?",
//         date: '2h ago',
//         commentCount: 3,
//         shareCount: 2,
//       },
//     ],
//   },
//   {
//     name: 'Popular',
//     posts: [
//       {
//         id: 1,
//         title: 'Is tech making coffee better or worse?',
//         date: 'Jan 7',
//         commentCount: 29,
//         shareCount: 16,
//       },
//       {
//         id: 2,
//         title: 'The most innovative things happening in coffee',
//         date: 'Mar 19',
//         commentCount: 24,
//         shareCount: 12,
//       },
//     ],
//   },
//   {
//     name: 'Trending',
//     posts: [
//       {
//         id: 1,
//         title: 'Ask Me Anything: 10 answers to your questions about coffee',
//         date: '2d ago',
//         commentCount: 9,
//         shareCount: 5,
//       },
//       {
//         id: 2,
//         title: "The worst advice we've ever heard about coffee",
//         date: '4d ago',
//         commentCount: 1,
//         shareCount: 2,
//       },
//     ],
//   },
// ]