import { Button, Dialog, DialogPanel, DialogTitle, Switch, Transition, TransitionChild } from '@headlessui/react';
import { Fragment, useState } from 'react';
import FileDrop from './fileDrop';

const AgentCard = ({ avatar, title, description, detailed_description}) => {
let [isOpen, setIsOpen] = useState(false);
let [enabled, setEnabled] = useState(true);

  function open() {
    setIsOpen(true)
  }

  function close() {
    setIsOpen(false)
  }

  async function handleTrigger() {
    console.log('🚀 Initiating API call with trigger',);
    let data = {
      topic: "trigger"
    };
    try {
      console.log('📡 Sending request to API...');
      const res = await fetch("https://f1e4-38-29-145-10.ngrok-free.app/whatsapp_message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      console.log('📥 Raw API response status:', res.status);
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const jsonResponse = await res.json();
      console.log('✅ Parsed API response structure:', {
        hasResult: !!jsonResponse.result,
        hasResponse: !!jsonResponse.result?.response,
        responseLength: jsonResponse.result?.response?.length
      });
      return jsonResponse;
    } catch (error) {
      console.error('❌ handleTrigger error:', {
        message: error.message,
        stack: error.stack,
        data: data
      });
      throw error;
    }
  }

  return (
    <>
        <Button
            onClick={open}
            className="min-h-24 max-h-40 min-w-80 max-w-80 w-40 h-30 flex border-solid border-black border-2 rounded-lg bg-white hover:shadow-xl transition duration-500"
        >
            {/* <div className="h-full w-full flex flex-row items-center">
                <div className="h-full max-w-20 ml-4 flex ">
                    <img 
                        src={avatar} 
                        alt="avatar" 
                        className="max-w-full max-h-full mt-4 mb-4 rounded-lg"
                    />
                </div>
                <div className='ml-6 flex flex-col items-stretch'>
                    <h1 className='ml-6 text-black font-roboto font-semibold text-lg w-full text-center truncate'>
                        {title}
                    </h1>
                    <p className='text-sm text-black w-full text-left truncate'>
                        {description}
                    </p>
                </div>
            </div> */}
          <div className="flex items-center justify-center w-1/3 my-3">
            <img
              src={avatar}
              alt="Agent"
              className="rounded-lg h-20 w-20 object-cover border-solid border-black border-2"
            />
          </div>
    
          {/* Right Section: Title and Description */}
          <div className="flex flex-col justify-center w-2/3 px-2">
            <h3 className="font-bold text-sm text-gray-800 truncate">{title}</h3>
            <p className="text-xs text-gray-600 mt-1 truncate">{description}</p>
          </div>
        </Button>
        {/* <Dialog open={isOpen} as="div" className="relative z-10 focus:outline-none" onClose={close}>
        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <DialogPanel
              transition
              className="w-full max-w-md rounded-xl bg-white/5 p-6 backdrop-blur-2xl duration-300 ease-out data-[closed]:transform-[scale(95%)] data-[closed]:opacity-0"
            >
              <DialogTitle as="h3" className="text-base/7 font-medium text-white">
                Payment successful
              </DialogTitle>
              <p className="mt-2 text-sm/6 text-white/50">
                Your payment has been successfully submitted. We’ve sent you an email with all of the details of your
                order.
              </p>
              <div className="mt-4">
                <Button
                  className="inline-flex items-center gap-2 rounded-md bg-gray-700 py-1.5 px-3 text-sm/6 font-semibold text-white shadow-inner shadow-white/10 focus:outline-none data-[hover]:bg-gray-600 data-[focus]:outline-1 data-[focus]:outline-white data-[open]:bg-gray-700"
                  onClick={close}
                >
                  Got it, thanks!
                </Button>
              </div>
            </DialogPanel>
          </div>
        </div>
      </Dialog> */}
        <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={close}>
          <TransitionChild
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black bg-opacity-25 backdrop-blur-sm" />
          </TransitionChild>

          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex items-center justify-center min-h-full p-4 text-center">
              <TransitionChild
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <DialogPanel className="w-full max-w-md mb-4 transform overflow-hidden rounded-lg bg-white p-6 text-left align-middle shadow-xl transition-all border-4 border-black">
                  <DialogTitle
                    as="h3"
                    className="text-2xl font-medium font-roboto leading-6 text-gray-900 text-center"
                  >
                    {title}
                  </DialogTitle>
                  <div className="mt-4 flex items-center">
                    <img
                      src={avatar}
                      alt="Profile"
                      className="w-24 h-24 rounded-lg"
                    />
                    <p className="ml-4 text-gray-500">
                      {detailed_description}
                    </p>
                  </div>
                  <div className="mt-4">
                    {/* <label className="block text-sm font-medium text-gray-700">
                      Upload Files
                    </label>
                    <input
                      type="file"
                      className="block w-full mt-2 border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    /> */}

                    {/* Old FileDrop begins here*/}
                    {/* <div className="flex items-center justify-center w-full border-2 border-black rounded-lg">
                      <label for="dropzone-file" className="flex flex-col items-center justify-center w-full h-32 rounded-lg cursor-pointer bg-white">
                        <div className="flex flex-col items-center justify-center pt-5 pb-6">
                          <svg className="w-8 h-8 mb-4 text-black" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                          </svg>
                          <p className="mb-2 text-sm text-black font-roboto">
                            <span className="font-semibold">Drag and drop relevant documents</span>
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-400 font-roboto">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
                        </div>
                        <input id="dropzone-file" type="file" className="hidden" />
                      </label>
                    </div>  */}

                    <FileDrop />
                  </div>
                  <div className="mt-4">
                    <label
                      htmlFor="description"
                      className="block text-sm pl-2 font-roboto font-medium text-gray-700"
                    >
                      How can I help?
                    </label>
                    <textarea
                      id="description"
                      className="block w-full mt-2 border-2 border-black rounded-lg p-2 resize-none focus:outline-none"
                      placeholder="Enter your text here..."
                    />
                  </div>
                  <div className="flex items-center space-x-4 mt-4">
                    <span className="text-sm font-medium">Connect to fleet?</span>
                      <Switch
                        checked={enabled}
                        onChange={setEnabled}
                        className={`${
                          enabled ? 'bg-black' : 'bg-white'
                        } relative inline-flex h-6 w-11 items-center rounded-full transition-colors border-2 border-black duration-200`}
                      >
                        <span
                          className={`${
                            enabled ? 'translate-x-6 bg-white' : 'translate-x-1 bg-black'
                          } inline-block h-4 w-4 transform rounded-full transition-transform duration-200`}
                        />
                      </Switch>
                    </div>
                  <div className="mt-6 flex justify-end space-x-2">
                    <button
                      type="button"
                      className="px-4 py-2 bg-white text-black border-2 border-black rounded-full hover:shadow-lg transition duration-400"
                      onClick={close}
                    >
                      Cancel
                    </button>
                    <button
                      type="button"
                      className="px-4 py-2 bg-black text-white rounded-full border-2 border-black hover:shadow-lg transition duration-400"
                      onClick={close}
                    >
                      Spawn
                    </button>
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </Transition>
    </>
  )
}

export default AgentCard;