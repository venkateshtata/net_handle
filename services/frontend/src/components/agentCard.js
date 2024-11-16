import { Button, Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import { useState } from 'react';

const AgentCard = ({ avatar, title, description}) => {
let [isOpen, setIsOpen] = useState(false);

  function open() {
    setIsOpen(true)
  }

  function close() {
    setIsOpen(false)
  }

  return (
    <>
        <Button
            onClick={open}
            className="max-h-30 min-w-40 max-w-80 w-40 h-30 flex border rounded-lg bg-white hover:shadow-md transition duration-500"
        >
            <div className="h-full w-full flex flex-row items-center">
                <div className="h-full max-w-10 ml-4 flex justify-center items-center">
                    <img 
                        src="https://img.freepik.com/free-psd/3d-illustration-person-with-sunglasses_23-2149436188.jpg?semt=ais_hybrid" 
                        alt="avatar" 
                        className="max-w-full max-h-full rounded-lg"
                    />
                </div>
                <div className='ml-6 h-full flex item-center flex-col'>
                    <h1 className='text-black text-sm'>
                        Medic Help
                    </h1>
                    <p className='text-sm text-black text-left'>
                        Lorem ipsum tota tota
                    </p>
                </div>
            </div>
        </Button>
        <Dialog open={isOpen} as="div" className="relative z-10 focus:outline-none" onClose={close}>
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
      </Dialog>
    </>
  )
}

export default AgentCard;