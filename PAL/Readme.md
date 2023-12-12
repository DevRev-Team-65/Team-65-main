The zip file contains all the necessary files, obtained directly from the source GitHub repo.
Added inference.py and backend.py, note that these are the modified files, the original files are in the zip.

The notebook can be used as a reference for what I've done as I used GoogleColab (obtained all the files by cloning then uploaded devrev_prompt.py manually) instead of running it locally.

NOTE: The code here is not publish-ready, some licenses and citations remain from the original authors, and they are to be removed.# Program-Aided-Language-Model
```InvalidRequestError                       Traceback (most recent call last)
<ipython-input-2-04baddafdaa3> in <cell line: 12>()
     10 question = "Find all tasks related to customer ABC Inc. and summarize them."
     11 prompt = devrev_prompt.DEVREV_PROMPT % question
---> 12 answer = interface.run(prompt)

/usr/local/lib/python3.10/dist-packages/openai/api_requestor.py in _interpret_response_line(self, rbody, rcode, rheaders, stream)
    773         stream_error = stream and "error" in resp.data
    774         if stream_error or not 200 <= rcode < 300:
--> 775             raise self.handle_error_response(
    776                 rbody, rcode, resp.data, rheaders, stream_error=stream_error
    777             )

InvalidRequestError: 'messages' is a required property```
