import * as React from 'react';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import { FixedSizeList, ListChildComponentProps } from 'react-window';

function renderRow(props: ListChildComponentProps, clickAction: (cell_index: number) => void) {
  const { data, index, style } = props;

  return (
    <ListItem style={style} key={index} component="div" disablePadding>
      <ListItemButton onClick={() => { clickAction(index) }}>
        <ListItemText primary={data[index]['title']} />
      </ListItemButton>
    </ListItem>
  );
}

interface VirtualizedListProps {
    clickAction     : (index: number) => void
    items           : []
}

export function VirtualizedList({ items, clickAction }: VirtualizedListProps) {
  return (
    <Box
      sx={{ width: '100%', height: '100%', maxWidth: 360, bgcolor: 'background.paper' }}
    >
      <FixedSizeList
        itemData={items}
        height={400}
        width={360}
        itemSize={50}
        itemCount={items.length}
        overscanCount={5}
      >
        {(props) => renderRow({...props}, clickAction=clickAction)}
      </FixedSizeList>
    </Box>
  );
}
