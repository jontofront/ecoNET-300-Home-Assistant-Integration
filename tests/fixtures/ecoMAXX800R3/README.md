# ecoMAXX800R3 fixture

Legacy ecoMAX pellet controller using the `em` protocol.

- Controller: `ecoMAXX800R3`
- ecoNET module software: `3.2.3879`
- No RM endpoints (`rmParamsData` empty)
- No `paramsEdits` (`rmCurrentDataParamsEdits` empty)
- Writable temperature setpoints come from `/econet/editParams` and are written
  with `/econet/newParam?newParamName=...`:
  - `CO_TEMP_SET`
  - `CWU_SET_TEMP`
  - `MIX_SET_TEMP_2`
  - `MIX_SET_TEMP_3`
