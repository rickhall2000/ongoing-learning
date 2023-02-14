import React, { useState } from 'react';
import Button from './Button'
import Label from './Label'

function ConversationUI ({setPromptText, promptText, responseText, resetFunction, makeConversation}) {
    return (
        <div className="container bg-gray-50 ml-20 shadow-md w-1/4">
            <div className='w-full px-2'>
                <Label>Prompt</Label>
                <textarea
                  value={promptText}
                  onChange={(event) => setPromptText(event.target.value)}
                          className="p-1 text-lg ring ring-gray-400 focus:bg-yellow-50 
                          focus:outline-none rounded w-full h-24"
                ></textarea>
            </div>
            <div className='w-full px-2'>
                <Button
                onClick={() => makeConversation(promptText)}
                >Send</Button>
            </div>
            <div className='w-full px-2'>
                <Label>Response</Label>
                <textarea
                    value={responseText}
                    readOnly={true}
                          className="p-1 text-lg ring ring-gray-400 focus:bg-yellow-50 
                          focus:outline-none rounded w-full h-24"
                ></textarea>
            </div>
            <div className='w-full px-2'>
                <Button onClick={resetFunction}>Clear</Button>
            </div>
        </div>
    )
}
export default ConversationUI;
