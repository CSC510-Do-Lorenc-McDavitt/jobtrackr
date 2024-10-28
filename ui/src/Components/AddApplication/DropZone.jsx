import React, { useRef } from 'react';
import { useDrop } from 'react-dnd';
import EditApplication from './EditApplication';
import axios from 'axios';
import { useState } from 'react';
import { Button, Card, Tag, Typography } from 'antd';


const DropZone = () => {
  const [{ canDrop, isOver }, drop] = useDrop({
    accept: 'CARD', // Specify the type of items you want to accept
    drop: (item) => {
      // Handle the dropped item here
      console.log('Dropped item:', item);
    },
    collect: (monitor) => ({
      canDrop: monitor.canDrop(),
      isOver: monitor.isOver(),
    }),
  });

  return (
    <div ref={drop} className={`droppable-zone ${canDrop ? 'can-drop' : ''} ${isOver ? 'is-over' : ''}`}>
      Drop here
    </div>
  );
};

export default DropZone;