import * as React from "react";
import Button from "@mui/material/Button";
import Dialog, { DialogProps } from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import ReactMarkdown from 'react-markdown'
import NotebookDownloadAlert from "./NotebookDownloadAlert"
import NotebookSendRatingAlert from "./NotebookSendRatingAlert"



interface NotebookDialogueProps {
  data: {[key: string]: any}
  query: string
}


export default function NotebookScrollDialog({ data, query }: NotebookDialogueProps) {

  const [open, setOpen] = React.useState(false);
  const [scroll] = React.useState<DialogProps["scroll"]>("paper");

  const handleClickOpen = (scrollType: DialogProps["scroll"]) => () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  
  const descriptionElementRef = React.useRef<HTMLElement>(null);
  React.useEffect(() => {
    if (open) {
      const { current: descriptionElement } = descriptionElementRef;
      if (descriptionElement !== null) {
        descriptionElement.focus();
      }
    }
  }, [open]);

  return (
    <div>
      <Button onClick={handleClickOpen("paper")}>More</Button>
      <Dialog
        open={open}
        onClose={handleClose}
        scroll={scroll}
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
      >
        <DialogTitle id="scroll-dialog-title">
          <div>
            <p>{data['name']}.</p>
            <p><a href={data['html_url']} target="_blank">{data['name']}</a>.</p>
          </div>
        </DialogTitle>
        <DialogContent dividers={true}>
          <DialogContentText
            id="scroll-dialog-description"
            ref={descriptionElementRef}
            tabIndex={-1}
          >
            <ReactMarkdown>{data['description']}</ReactMarkdown>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <NotebookSendRatingAlert
                                        data = {data}
                                        query= {query}/>

          <NotebookDownloadAlert
                                        data = {data}
                                        query= {query}/>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}