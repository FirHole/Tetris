def main(pieces, mode):
      figures = [
        {
        'o': [[1]],

        '2I': [[1, 1]],

        '3I': [[1, 1, 1]],

        'v': [[1, 0],
              [1, 1]],

        
        },
        
        {
        'z': [[1, 1, 0],
              [0, 1, 1]],

        's': [[0, 1, 1],
              [1, 1, 0]],

        '4I': [[1, 1, 1, 1]],

        'l': [[0, 0, 1],
              [1, 1, 1]],

        'j': [[1, 0, 0],
              [1, 1, 1]],

        't': [[0, 1, 0],
              [1, 1, 1]],

        'O': [[1, 1],
              [1, 1]]
    },

    {
        '5I': [[1, 1, 1, 1, 1]],

        'T': [[1, 1, 1],
              [0, 1, 0],
              [0, 1, 0]],

        'U': [[1, 0, 1],
              [1, 1, 1]],

        'V': [[1, 0, 0],
              [1, 0, 0],
              [1, 1, 1]],

        'W': [[1, 0, 0],
              [1, 1, 0],
              [0, 1, 1]],

        'X': [[0, 1, 0],
              [1, 1, 1],
              [0, 1, 0]],

        'f': [[1, 0, 0],
              [1, 1, 1],
              [0, 1, 0]],

        "f'": [[0, 0, 1],
               [1, 1, 1],
               [0, 1, 0]],

        'S': [[0, 1, 1],
              [0, 1, 0],
              [1, 1, 0]],

        'Z': [[1, 1, 0],
              [0, 1, 0],
              [0, 1, 1]],

        'J': [[1, 0, 0, 0],
              [1, 1, 1, 1]],
        
        'L': [[0, 0, 0, 1],
              [1, 1, 1, 1]],

        "Y'": [[0, 1, 0, 0],
              [1, 1, 1, 1]],

        'Y': [[0, 0, 1, 0],
              [1, 1, 1, 1]],

        'h': [[0, 0, 1, 1],
              [1, 1, 1, 0]],

        'N': [[1, 1, 0, 0],
              [0, 1, 1, 1]],

        'P': [[1, 1, 0],
              [1, 1, 1]],
              
        'Q': [[0, 1, 1],
              [1, 1, 1]]
    }]

      linear = ['o', '2I', '3I', 'v', '4I', 'l', 'j', '5I', 'V', 'J', 'L']
      size = [0.5, 1, 1.5]

      request = {}
      for i in pieces:
            request.update(figures[i])

      if mode == 1:
            old_request = request.copy().items()
            request = {}
            for key, value in old_request:
                  if key in linear:
                        request.update({key : value})


      return request, size[i]